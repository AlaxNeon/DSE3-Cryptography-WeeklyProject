"""
falcon_demo.py
==============

Digital-signature logic for the Week-3 demonstration.

This module tries to use a REAL Falcon implementation (Falcon-512, via the
`liboqs-python` bindings to the Open Quantum Safe `liboqs` C library). If
that real implementation is not available in the current environment (for
example, the system is missing `cmake` / a C compiler / `git`, or the
one-time native build fails), the module automatically falls back to a
clearly labelled EDUCATIONAL SIMULATION that is NOT real Falcon and is NOT
cryptographically secure. It exists only to demonstrate the sign/verify/
tamper-detection workflow.

You can force a specific mode with an environment variable:

    FALCON_DEMO_MODE=real          # require the real Falcon library
    FALCON_DEMO_MODE=simulation    # always use the fast educational simulation
    FALCON_DEMO_MODE=auto          # (default) try real, fall back automatically

Public interface (used by main.py and the tests):

    generate_keys()                    -> public_key: bytes
    sign_message(message: bytes)       -> signature: bytes
    verify_signature(message, sig)     -> bool
    get_mode_description()             -> str  (human-readable status)
    USING_REAL_FALCON                  -> bool
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

FALCON_ALGORITHM = "Falcon-512"

# ---------------------------------------------------------------------------
# Mode selection
# ---------------------------------------------------------------------------

import os

_MODE_OVERRIDE = os.environ.get("FALCON_DEMO_MODE", "auto").strip().lower()

_oqs = None  # will hold the imported `oqs` module if real Falcon is usable
USING_REAL_FALCON = False
_REAL_FALCON_UNAVAILABLE_REASON = ""


def _attempt_load_real_falcon() -> bool:
    """Try to import and sanity-check the real Falcon backend (liboqs-python).

    Returns True only if the library imports AND reports Falcon-512 as an
    enabled signature mechanism. Any failure along the way is treated as
    "real Falcon is not available here" rather than crashing the program,
    because the whole point of this project is to still run for a beginner
    who has not installed a C toolchain.
    """
    global _oqs, _REAL_FALCON_UNAVAILABLE_REASON

    if _MODE_OVERRIDE == "simulation":
        _REAL_FALCON_UNAVAILABLE_REASON = "simulation mode forced by FALCON_DEMO_MODE"
        return False

    try:
        import oqs as _oqs_module  # noqa: F401  (liboqs-python)
    except (ImportError, RuntimeError, SystemExit, OSError) as exc:
        _REAL_FALCON_UNAVAILABLE_REASON = f"could not import/build liboqs-python ({exc})"
        return False
    except Exception as exc:  # pragma: no cover - defensive catch-all
        _REAL_FALCON_UNAVAILABLE_REASON = f"unexpected error loading liboqs-python ({exc})"
        return False

    try:
        enabled = _oqs_module.get_enabled_sig_mechanisms()
    except Exception as exc:  # pragma: no cover - defensive catch-all
        _REAL_FALCON_UNAVAILABLE_REASON = f"liboqs loaded but could not list algorithms ({exc})"
        return False

    if FALCON_ALGORITHM not in enabled:
        _REAL_FALCON_UNAVAILABLE_REASON = (
            f"{FALCON_ALGORITHM} is not enabled in this liboqs build"
        )
        return False

    _oqs = _oqs_module
    return True


USING_REAL_FALCON = _attempt_load_real_falcon()

if _MODE_OVERRIDE == "real" and not USING_REAL_FALCON:
    raise RuntimeError(
        "FALCON_DEMO_MODE=real was requested, but the real Falcon backend "
        f"(liboqs-python) is not available: {_REAL_FALCON_UNAVAILABLE_REASON}\n"
        "Install the prerequisites described in README.md (cmake, a C compiler, "
        "git, OpenSSL development headers), then `pip install -r requirements.txt` "
        "again, or drop FALCON_DEMO_MODE to let the project fall back to the "
        "educational simulation."
    )


def get_mode_description() -> str:
    """Return a short, human-readable description of the active mode."""
    if USING_REAL_FALCON:
        return (
            f"REAL Falcon implementation in use ({FALCON_ALGORITHM}, via the "
            "liboqs-python bindings to the Open Quantum Safe liboqs library)."
        )
    return (
        "Educational Falcon Concept Simulation in use "
        "(NOT a real Falcon cryptographic implementation). "
        f"Reason real Falcon was not used: {_REAL_FALCON_UNAVAILABLE_REASON}"
    )


# ---------------------------------------------------------------------------
# State held by this module for the lifetime of one demo run
# ---------------------------------------------------------------------------

_real_signer = None          # oqs.Signature instance holding the secret key (real mode)
_public_key: bytes | None = None
_sim_private_key: bytes | None = None  # simulation-mode "private key" (never printed)


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def generate_keys() -> bytes:
    """Generate a fresh keypair and return the PUBLIC key only.

    The private/secret key material is kept inside this module and is never
    printed or returned, matching how a real signature system should behave.
    """
    global _real_signer, _public_key, _sim_private_key

    if USING_REAL_FALCON:
        _real_signer = _oqs.Signature(FALCON_ALGORITHM)
        _public_key = _real_signer.generate_keypair()
    else:
        # Educational simulation: a random 32-byte "private key" and a
        # derived "public key". This is a toy construction for teaching the
        # sign/verify workflow only -- it is not a real public-key scheme.
        _sim_private_key = secrets.token_bytes(32)
        _public_key = hashlib.sha256(_sim_private_key).digest()

    return _public_key


def hash_message(message: bytes) -> str:
    """Return a SHA-256 hex digest of the message (used before signing)."""
    return hashlib.sha256(message).hexdigest()


def sign_message(message: bytes) -> bytes:
    """Sign `message` (bytes) and return the signature (bytes)."""
    if _public_key is None:
        raise RuntimeError("Call generate_keys() before sign_message().")

    if USING_REAL_FALCON:
        return _real_signer.sign(message)

    # Educational simulation: an HMAC-SHA256 tag computed with the toy
    # private key. This demonstrates "only the key holder can produce a
    # valid tag, and any change to the message invalidates it" without
    # claiming to be a real asymmetric lattice signature.
    return hmac.new(_sim_private_key, message, hashlib.sha256).digest()


def verify_signature(message: bytes, signature: bytes) -> bool:
    """Verify `signature` over `message` using the stored public key.

    Returns True if valid, False otherwise. Never raises for a malformed or
    mismatched signature -- verification failure is reported as False, the
    same way a real verifier would report "invalid", not a crash.
    """
    if _public_key is None:
        raise RuntimeError("Call generate_keys() before verify_signature().")

    if USING_REAL_FALCON:
        verifier = _oqs.Signature(FALCON_ALGORITHM)
        try:
            return bool(verifier.verify(message, signature, _public_key))
        except Exception:
            # A malformed signature (wrong length, corrupted bytes, etc.)
            # is simply an invalid signature from the caller's point of view.
            return False
        finally:
            free = getattr(verifier, "free", None)
            if callable(free):
                free()

    expected = hmac.new(_sim_private_key, message, hashlib.sha256).digest()
    return hmac.compare_digest(expected, signature)
