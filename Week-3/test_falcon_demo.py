"""
test_falcon_demo.py
====================

Unit tests for falcon_demo.py, using Python's built-in `unittest`.

Run with:

    python -m unittest test_falcon_demo.py

These tests run against whichever backend falcon_demo selects (real Falcon
or the educational simulation), so they pass either way -- what matters is
that the *behavior* of the signature workflow is correct: valid signatures
verify, tampered messages fail, and wrong signatures are rejected.
"""

import unittest

import falcon_demo


class TestFalconDemo(unittest.TestCase):
    def setUp(self) -> None:
        # A fresh keypair for each test keeps tests independent of each
        # other and of test execution order.
        self.public_key = falcon_demo.generate_keys()
        self.message = b"Device ID: ESP32-01, Temperature: 28.5 C"

    # Test 1 -- Key generation
    def test_key_generation(self) -> None:
        self.assertIsInstance(self.public_key, (bytes, bytearray))
        self.assertGreater(len(self.public_key), 0)

    # Test 2 -- Signature generation
    def test_signature_generation(self) -> None:
        signature = falcon_demo.sign_message(self.message)
        self.assertIsInstance(signature, (bytes, bytearray))
        self.assertGreater(len(signature), 0)

    # Test 3 -- Valid signature verifies successfully
    def test_valid_signature_passes(self) -> None:
        signature = falcon_demo.sign_message(self.message)
        self.assertTrue(falcon_demo.verify_signature(self.message, signature))

    # Test 4 -- A modified message must fail verification
    def test_modified_message_fails(self) -> None:
        signature = falcon_demo.sign_message(self.message)
        tampered_message = self.message.replace(b"28.5", b"98.5")
        self.assertFalse(
            falcon_demo.verify_signature(tampered_message, signature)
        )

    # Test 5 -- A corrupted/wrong signature must be rejected
    def test_wrong_signature_is_rejected(self) -> None:
        signature = falcon_demo.sign_message(self.message)
        # Flip one bit in the first byte to create an invalid signature of
        # the same length (this avoids library-specific errors that could
        # otherwise be raised for a signature of the wrong length).
        corrupted = bytearray(signature)
        corrupted[0] ^= 0xFF
        self.assertFalse(
            falcon_demo.verify_signature(self.message, bytes(corrupted))
        )

    # Test 6 -- An empty message is handled cleanly
    def test_empty_message(self) -> None:
        empty_message = b""
        signature = falcon_demo.sign_message(empty_message)
        self.assertTrue(falcon_demo.verify_signature(empty_message, signature))
        # Verifying the empty message against a signature made for the
        # non-empty message should fail.
        other_signature = falcon_demo.sign_message(self.message)
        self.assertFalse(
            falcon_demo.verify_signature(empty_message, other_signature)
        )


if __name__ == "__main__":
    unittest.main()
