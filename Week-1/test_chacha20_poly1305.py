"""
test_chacha20_poly1305.py
--------------------------
Beginner-friendly unit tests for chacha20_poly1305.py

Run with:
    python -m unittest test_chacha20_poly1305.py
"""

import unittest

from cryptography.exceptions import InvalidTag

from chacha20_poly1305 import (
    generate_key,
    generate_nonce,
    encrypt_message,
    decrypt_message,
)


class TestChaCha20Poly1305(unittest.TestCase):

    def setUp(self):
        # Runs before every test - gives each test a fresh key/nonce/data.
        self.key = generate_key()
        self.nonce = generate_nonce()
        self.plaintext = b"Temperature: 28.5 C, Humidity: 65%"
        self.aad = b"Device-ID: ESP32-01"

    def test_encrypt_then_decrypt_returns_original_plaintext(self):
        """Test 1: Encryption followed by decryption should give back the
        exact original plaintext."""
        ciphertext = encrypt_message(self.key, self.plaintext, self.nonce, self.aad)
        recovered = decrypt_message(self.key, ciphertext, self.nonce, self.aad)
        self.assertEqual(recovered, self.plaintext)

    def test_correct_aad_allows_successful_decryption(self):
        """Test 2: Using the same, correct AAD on both sides should allow
        decryption to succeed."""
        ciphertext = encrypt_message(self.key, self.plaintext, self.nonce, self.aad)
        # Using the exact same AAD again here (as the receiver would):
        recovered = decrypt_message(self.key, ciphertext, self.nonce, self.aad)
        self.assertEqual(recovered, self.plaintext)

    def test_modified_ciphertext_fails_authentication(self):
        """Test 3: Changing even one byte of the ciphertext should cause
        decryption to fail with InvalidTag."""
        ciphertext = encrypt_message(self.key, self.plaintext, self.nonce, self.aad)

        tampered = bytearray(ciphertext)
        tampered[0] ^= 0xFF  # flip bits in the first byte
        tampered_ciphertext = bytes(tampered)

        with self.assertRaises(InvalidTag):
            decrypt_message(self.key, tampered_ciphertext, self.nonce, self.aad)

    def test_modified_aad_fails_authentication(self):
        """Test 4: Changing the AAD between encryption and decryption
        should cause authentication to fail, even if the ciphertext itself
        was not touched."""
        ciphertext = encrypt_message(self.key, self.plaintext, self.nonce, self.aad)

        wrong_aad = b"Device-ID: ESP32-99"

        with self.assertRaises(InvalidTag):
            decrypt_message(self.key, ciphertext, self.nonce, wrong_aad)

    def test_different_nonce_produces_different_ciphertext(self):
        """Test 5: Encrypting the same plaintext with the same key but a
        different nonce should produce a different ciphertext."""
        nonce_a = generate_nonce()
        nonce_b = generate_nonce()

        ciphertext_a = encrypt_message(self.key, self.plaintext, nonce_a, self.aad)
        ciphertext_b = encrypt_message(self.key, self.plaintext, nonce_b, self.aad)

        self.assertNotEqual(ciphertext_a, ciphertext_b)


if __name__ == "__main__":
    unittest.main()
