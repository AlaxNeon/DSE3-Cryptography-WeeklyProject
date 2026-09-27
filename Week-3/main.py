"""
main.py
=======

Entry point for the Week-3 demonstration:

    Post-Quantum Falcon Signature Scheme: Fast Fourier Lattice Signatures

Run it with:

    python main.py

This script walks through the full workflow described in the README:
prepare a message, hash it, sign it, verify it, tamper with it, and verify
again to show that tampering is detected. It also runs a small standalone
FFT demonstration to illustrate the computational idea behind Falcon's
efficient implementation.
"""

from __future__ import annotations

import falcon_demo
import fft_demo


LINE = "=" * 56


def banner(text: str) -> None:
    print(LINE)
    print(text)
    print(LINE)


def section(text: str) -> None:
    print()
    print(text)


def run_signature_demo() -> None:
    banner("Week-3: Post-Quantum Falcon Signature Demonstration")

    print()
    print("IMPORTANT:")
    print("This project is an educational demonstration.")
    print("It does not implement Falcon cryptography from scratch.")
    print(f"Mode: {falcon_demo.get_mode_description()}")

    # Step 1: Initialize the signature system
    section("[1] Initializing signature system...")
    public_key = falcon_demo.generate_keys()
    print(f"Public key generated ({len(public_key)} bytes).")
    print("Private key: [hidden]")

    # Step 2: Create a sample IoT message
    section("[2] Preparing IoT message...")
    message_text = (
        "Device ID: ESP32-01\n"
        "Temperature: 28.5 C\n"
        "Humidity: 65%\n"
        "Battery: 87%"
    )
    print("Message:")
    print(message_text)
    message_bytes = message_text.encode("utf-8")

    # Step 3: Hash the message
    section("[3] Creating message hash...")
    digest = falcon_demo.hash_message(message_bytes)
    print("Hash:")
    print(digest)

    # Step 4: Generate a digital signature
    section("[4] Generating digital signature...")
    signature = falcon_demo.sign_message(message_bytes)
    print(f"Signature generated successfully ({len(signature)} bytes).")

    # Step 5: Verify the original message
    section("[5] Verifying original message...")
    original_valid = falcon_demo.verify_signature(message_bytes, signature)
    if original_valid:
        print("Signature verification: SUCCESS")
        print("The message is authentic.")
    else:
        print("Signature verification: FAILED")
        print("Something is wrong -- the original message should verify.")

    # Step 6: Tamper with the message
    section("[6] Tampering demonstration...")
    tampered_text = message_text.replace("Temperature: 28.5 C", "Temperature: 98.5 C")
    print("Modified message:")
    print("Temperature: 98.5 C")
    tampered_bytes = tampered_text.encode("utf-8")

    # Step 7: Verify the modified message (same signature, changed message)
    section("[7] Verifying modified message...")
    tampered_valid = falcon_demo.verify_signature(tampered_bytes, signature)
    if tampered_valid:
        print("Signature verification: SUCCESS (unexpected!)")
    else:
        print("Signature verification: FAILED")
        print("The modification was detected.")

    # Step 8: Clear summary
    section("[8] Summary")
    print(f"Original message:  {'VALID' if original_valid else 'INVALID'}")
    print(f"Modified message:  {'VALID' if tampered_valid else 'INVALID'}")
    print("Tampering detected." if (original_valid and not tampered_valid) else "")


def run_fft_demo() -> None:
    print()
    banner("Bonus: Fast Fourier Transform (FFT) Demonstration")
    print()
    fft_demo.demonstrate_fft()


def main() -> None:
    run_signature_demo()
    run_fft_demo()
    print()
    banner("Week-3 demonstration completed successfully.")


if __name__ == "__main__":
    main()
