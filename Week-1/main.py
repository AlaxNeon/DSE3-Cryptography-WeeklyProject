"""
main.py
-------
Week-1 demonstration of ChaCha20-Poly1305 AEAD encryption.

This script simulates a very simple IoT scenario:

    Sensor (plaintext)
        -> Encryption (ChaCha20-Poly1305)
        -> Ciphertext sent over "network"
        -> Decryption (ChaCha20-Poly1305)
        -> Receiver recovers original data

It also demonstrates what happens if the ciphertext is tampered with while
"in transit" - decryption should fail loudly (but cleanly, no ugly crash).

Run it with:
    python main.py
"""

from cryptography.exceptions import InvalidTag

from chacha20_poly1305 import (
    generate_key,
    generate_nonce,
    encrypt_message,
    decrypt_message,
)


def line():
    print("=" * 40)


def main():
    line()
    print("Week-1: ChaCha20-Poly1305 AEAD Demo")
    line()
    print()

    # -----------------------------------------------------------------
    # Step 1: Key generation
    # -----------------------------------------------------------------
    print("[1] Generating 256-bit key...")
    key = generate_key()
    print("Key generated successfully.")
    print(f"Key (hex): {key.hex()}")
    print()

    # -----------------------------------------------------------------
    # Step 2: Nonce generation
    # -----------------------------------------------------------------
    print("[2] Generating nonce...")
    nonce = generate_nonce()
    print("Nonce generated successfully.")
    print(f"Nonce (hex): {nonce.hex()}")
    print()

    # -----------------------------------------------------------------
    # Step 3: Simulated IoT sensor data (plaintext)
    # -----------------------------------------------------------------
    plaintext = b"Temperature: 28.5 C, Humidity: 65%"
    print("[3] Original IoT Sensor Data:")
    print(plaintext.decode())
    print()

    # -----------------------------------------------------------------
    # Step 4: Additional Authenticated Data (AAD)
    # -----------------------------------------------------------------
    # AAD is authenticated (protected from tampering) but NOT encrypted.
    # A real device might attach its ID this way, so the receiver can be
    # sure both the data AND the sender's identity were not tampered with,
    # even though the device ID itself is not secret.
    aad = b"Device-ID: ESP32-01"
    print("[4] Additional Authenticated Data:")
    print(aad.decode())
    print()

    # -----------------------------------------------------------------
    # Step 5: Encryption
    # -----------------------------------------------------------------
    print("[5] Encrypting...")
    ciphertext = encrypt_message(key, plaintext, nonce, aad)
    print("Encryption successful.")
    print()
    print("Ciphertext (hex):")
    print(ciphertext.hex())
    print()
    print("Nonce (hex):")
    print(nonce.hex())
    print()

    # -----------------------------------------------------------------
    # Step 6: Decryption (the "happy path" - nothing was tampered with)
    # -----------------------------------------------------------------
    print("[6] Decrypting...")
    try:
        recovered_plaintext = decrypt_message(key, ciphertext, nonce, aad)
        print("Decryption successful.")
        print()
        print("Recovered plaintext:")
        print(recovered_plaintext.decode())
    except InvalidTag:
        # This branch should not happen on the happy path, but we handle
        # it anyway so the program never crashes with a raw traceback.
        print("Authentication failed! The message may have been modified.")
    print()

    # -----------------------------------------------------------------
    # Step 7: Tamper detection demonstration
    # -----------------------------------------------------------------
    print("[7] Testing Tamper Detection...")
    print("Modifying ciphertext...")

    # Flip one byte of the ciphertext to simulate an attacker (or network
    # error) corrupting the message in transit.
    tampered = bytearray(ciphertext)
    tampered[0] ^= 0xFF  # flip all bits in the first byte
    tampered_ciphertext = bytes(tampered)

    try:
        decrypt_message(key, tampered_ciphertext, nonce, aad)
        # If we ever get here, something is wrong - tampering should have
        # been detected.
        print("ERROR: Tampering was NOT detected! This should not happen.")
    except InvalidTag:
        print()
        print("Authentication failed!")
        print("The message was detected as modified.")
    print()

    line()
    print("Demo completed successfully.")
    line()


if __name__ == "__main__":
    main()
