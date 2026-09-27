"""
chacha20_poly1305.py
---------------------
Simple helper functions for ChaCha20-Poly1305 AEAD encryption.

AEAD = Authenticated Encryption with Associated Data.

ChaCha20-Poly1305 provides both:
1. Confidentiality - hides the message (nobody can read it without the key)
2. Integrity/authentication - detects if the message (or ciphertext) was
   modified in any way

We do NOT implement the ChaCha20 stream cipher or the Poly1305 authenticator
ourselves. Instead, we use the well-tested implementation provided by the
Python `cryptography` library.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

# ChaCha20-Poly1305 always uses a 12-byte (96-bit) nonce.
# A "nonce" is a Number used ONCE - it must never repeat for the same key.
NONCE_SIZE = 12


def generate_key():
    """
    Generate a new random 256-bit (32-byte) secret key.

    This uses the library's own secure random key-generation method, so we
    never have to think about how "random" is random enough - the library
    handles that for us.
    """
    # ChaCha20Poly1305.generate_key() returns 32 random bytes (256 bits).
    return ChaCha20Poly1305.generate_key()


def generate_nonce():
    """
    Generate a fresh, random 12-byte nonce.

    IMPORTANT: A new nonce must be generated for every single encryption
    operation that uses the same key. Reusing a (key, nonce) pair breaks
    the security guarantees of ChaCha20-Poly1305 - an attacker could
    potentially recover information about the plaintexts or forge messages.
    """
    return os.urandom(NONCE_SIZE)


def encrypt_message(key, plaintext, nonce, aad=None):
    """
    Encrypt `plaintext` using ChaCha20-Poly1305.

    Parameters:
        key       -- 32-byte secret key (bytes)
        plaintext -- the message to encrypt (bytes)
        nonce     -- 12-byte nonce, unique for this key (bytes)
        aad       -- Additional Authenticated Data (bytes or None).
                     AAD is authenticated (protected against tampering)
                     but is NOT encrypted, and is NOT included in the
                     returned ciphertext - the receiver must already know
                     it (or receive it separately) and pass the exact
                     same AAD in when decrypting.

    Returns:
        ciphertext -- the encrypted message, with the authentication
                      tag appended at the end (this is how the
                      `cryptography` library's AEAD classes work).
    """
    chacha = ChaCha20Poly1305(key)

    # .encrypt() runs ChaCha20 to scramble the plaintext AND runs Poly1305
    # to compute an authentication tag over the ciphertext + AAD. The tag
    # is appended to the returned ciphertext automatically.
    ciphertext = chacha.encrypt(nonce, plaintext, aad)
    return ciphertext


def decrypt_message(key, ciphertext, nonce, aad=None):
    """
    Decrypt `ciphertext` using ChaCha20-Poly1305 and verify authenticity.

    Parameters:
        key        -- the same 32-byte secret key used for encryption
        ciphertext -- the encrypted message (including the auth tag)
        nonce      -- the same nonce that was used for encryption
        aad        -- the same Additional Authenticated Data used for
                      encryption (or None if none was used)

    Returns:
        plaintext -- the original decrypted message (bytes), ONLY if the
                     authentication tag is valid.

    Raises:
        cryptography.exceptions.InvalidTag -- if the ciphertext, nonce,
        key, or AAD do not match what was used during encryption. This is
        exactly what happens if someone has tampered with the message.
    """
    chacha = ChaCha20Poly1305(key)

    # .decrypt() first checks the Poly1305 authentication tag. If it does
    # not match, it raises InvalidTag and refuses to return any plaintext
    # at all - this is what protects us from tampered/forged messages.
    plaintext = chacha.decrypt(nonce, ciphertext, aad)
    return plaintext


# Re-export InvalidTag here so other files can catch it without needing to
# know the exact import path inside the `cryptography` library.
__all__ = [
    "generate_key",
    "generate_nonce",
    "encrypt_message",
    "decrypt_message",
    "InvalidTag",
    "NONCE_SIZE",
]
