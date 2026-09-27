"""
test_secure_enclave.py

Simple unit tests for the SecureEnclave simulation.

Run these tests with:

    python -m unittest test_secure_enclave.py

or simply:

    python -m unittest
"""

import unittest
from secure_enclave import SecureEnclave


class TestSecureEnclave(unittest.TestCase):

    # ------------------------------------------------------------
    # Test 1: Enclave Creation
    # ------------------------------------------------------------
    def test_1_enclave_creation(self):
        """The simulated enclave should be created without errors."""
        enclave = SecureEnclave()
        self.assertIsInstance(enclave, SecureEnclave)

    # ------------------------------------------------------------
    # Test 2: Data Loading
    # ------------------------------------------------------------
    def test_2_data_loading(self):
        """Sensor data should load without raising an exception."""
        enclave = SecureEnclave()
        try:
            enclave.load_data([28.5, 29.1, 27.8, 30.2, 28.9])
        except Exception as error:
            self.fail(f"load_data() raised an unexpected exception: {error}")

    # ------------------------------------------------------------
    # Test 3: Average Calculation
    # ------------------------------------------------------------
    def test_3_average_calculation(self):
        """The average of known values should be calculated correctly."""
        enclave = SecureEnclave()
        enclave.load_data([10, 20, 30])
        self.assertEqual(enclave.compute_average(), 20)

    # ------------------------------------------------------------
    # Test 4: Minimum Calculation
    # ------------------------------------------------------------
    def test_4_minimum_calculation(self):
        """The minimum of known values should be calculated correctly."""
        enclave = SecureEnclave()
        enclave.load_data([10, 20, 30])
        self.assertEqual(enclave.compute_minimum(), 10)

    # ------------------------------------------------------------
    # Test 5: Maximum Calculation
    # ------------------------------------------------------------
    def test_5_maximum_calculation(self):
        """The maximum of known values should be calculated correctly."""
        enclave = SecureEnclave()
        enclave.load_data([10, 20, 30])
        self.assertEqual(enclave.compute_maximum(), 30)

    # ------------------------------------------------------------
    # Test 6: Integrity Verification (unchanged data passes)
    # ------------------------------------------------------------
    def test_6_integrity_verification_passes(self):
        """Unchanged data should pass the integrity check."""
        enclave = SecureEnclave()
        enclave.load_data([28.5, 29.1, 27.8, 30.2, 28.9])
        self.assertTrue(enclave.verify_integrity())

    # ------------------------------------------------------------
    # Test 7: Tampering Detection
    # ------------------------------------------------------------
    def test_7_tampering_detection(self):
        """Modified internal data should fail the integrity check."""
        enclave = SecureEnclave()
        enclave.load_data([28.5, 29.1, 27.8, 30.2, 28.9])

        # Simulate tampering with the internal data.
        enclave.simulate_external_tampering(index=2, new_value=97.8)

        self.assertFalse(enclave.verify_integrity())


if __name__ == "__main__":
    unittest.main()
