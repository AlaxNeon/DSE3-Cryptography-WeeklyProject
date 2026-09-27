"""
secure_enclave.py

This file contains a SIMPLE SOFTWARE SIMULATION of an Intel SGX-style
"secure enclave".

IMPORTANT:
This is NOT a real Intel SGX enclave. It does not use any special CPU
instructions, and it does not provide real hardware-backed memory
isolation. It only uses normal Python "private" attributes (name
mangling with double underscores) to demonstrate the IDEA of an
enclave that keeps sensitive data hidden from the rest of the program.

Think of this class as a small "black box":
    - You can put sensitive data IN.
    - You can ask it to compute something.
    - You get a RESULT out.
    - You never get direct access to the raw sensitive data again.
"""

import hashlib


class SecureEnclave:
    """
    A simulated secure enclave.

    In real Intel SGX, sensitive data would live inside a hardware
    protected memory region (the "enclave"), and even the operating
    system could not read it directly.

    Here, we simulate that idea using a "private" attribute
    (self.__sensitive_data). Python does not provide real memory
    protection, but the double-underscore naming makes it clear that
    this attribute is meant to be internal/private to the class, and
    it is not directly reachable from outside using the normal
    attribute name (Python performs "name mangling" on it).
    """

    def __init__(self):
        # The sensitive data starts empty until something is loaded.
        self.__sensitive_data = None

        # This will store the SHA-256 hash of the data, used later
        # to check if the data has been changed ("integrity check").
        self.__integrity_hash = None

        # A simple flag so we know if data has been loaded yet.
        self.__data_loaded = False

    # ------------------------------------------------------------------
    # Step 1: Load sensitive data into the enclave
    # ------------------------------------------------------------------
    def load_data(self, data):
        """
        Load sensitive data into the simulated enclave.

        'data' should be a list of numbers (for example, temperature
        sensor readings). Once loaded, this data is treated as
        "inside the enclave" and should not be read directly by the
        normal application code.
        """
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Sensitive data must be a non-empty list of numbers.")

        # Store a copy of the data internally (simulated enclave memory).
        self.__sensitive_data = list(data)

        # Immediately calculate an integrity hash of the data.
        self.__integrity_hash = self.__calculate_hash(self.__sensitive_data)

        self.__data_loaded = True

    # ------------------------------------------------------------------
    # Internal helper: calculate a SHA-256 hash of the data
    # ------------------------------------------------------------------
    def __calculate_hash(self, data):
        """
        Calculate a SHA-256 hash of the given data.

        NOTE: SHA-256 here is used only to demonstrate INTEGRITY
        VERIFICATION (detecting if data changed). It is NOT
        encryption, and it does not hide the data or provide any
        real hardware security.
        """
        # Convert the list of numbers into a consistent string format
        # so that hashing produces the same result for the same data.
        data_string = ",".join(str(value) for value in data)

        # Encode the string into bytes, then hash it with SHA-256.
        data_bytes = data_string.encode("utf-8")
        hash_object = hashlib.sha256(data_bytes)

        return hash_object.hexdigest()

    # ------------------------------------------------------------------
    # Step 2: Verify that the sensitive data has not been tampered with
    # ------------------------------------------------------------------
    def verify_integrity(self):
        """
        Recalculate the hash of the current internal data and compare
        it to the hash that was stored when the data was first loaded.

        Returns True if the data is unchanged, False if it appears to
        have been modified.
        """
        if not self.__data_loaded:
            raise RuntimeError("No data has been loaded into the enclave yet.")

        current_hash = self.__calculate_hash(self.__sensitive_data)
        return current_hash == self.__integrity_hash

    # ------------------------------------------------------------------
    # Step 3: Perform confidential computation inside the enclave
    # ------------------------------------------------------------------
    def compute_average(self):
        """Compute the average of the sensitive data, inside the enclave."""
        self.__require_data_loaded()
        return sum(self.__sensitive_data) / len(self.__sensitive_data)

    def compute_minimum(self):
        """Compute the minimum value of the sensitive data."""
        self.__require_data_loaded()
        return min(self.__sensitive_data)

    def compute_maximum(self):
        """Compute the maximum value of the sensitive data."""
        self.__require_data_loaded()
        return max(self.__sensitive_data)

    def __require_data_loaded(self):
        """Internal helper to make sure data has been loaded first."""
        if not self.__data_loaded:
            raise RuntimeError("No data has been loaded into the enclave yet.")

    # ------------------------------------------------------------------
    # Simulated "tampering" for demonstration purposes only
    # ------------------------------------------------------------------
    def simulate_external_tampering(self, index, new_value):
        """
        FOR DEMONSTRATION ONLY.

        In a real system, an attacker should NOT be able to reach into
        enclave memory and change it. This method exists only so that
        our demonstration program (main.py) can show what happens when
        the internal data is modified without going through the normal
        load_data() method - the integrity check should then fail.

        This method directly modifies the "private" attribute using
        Python's name-mangled access, purely to simulate an attacker
        or a bug corrupting the data behind the enclave's back.
        """
        if not self.__data_loaded:
            raise RuntimeError("No data has been loaded into the enclave yet.")

        if index < 0 or index >= len(self.__sensitive_data):
            raise IndexError("Index out of range for sensitive data.")

        self.__sensitive_data[index] = new_value
        # Notice: we do NOT update self.__integrity_hash here.
        # That is exactly why verify_integrity() will detect the change.

    # ------------------------------------------------------------------
    # Demonstrating that the application cannot directly read the data
    # ------------------------------------------------------------------
    def attempt_direct_access(self):
        """
        Try to access the sensitive data the "normal" way, using the
        public attribute name a caller might guess (sensitive_data).

        This will always fail with an AttributeError, because Python's
        name mangling means the real attribute is actually stored as
        '_SecureEnclave__sensitive_data', not 'sensitive_data'.

        This method exists only to clearly DEMONSTRATE that direct
        access is blocked - it deliberately triggers the error and
        returns a friendly message instead of crashing the program.
        """
        try:
            # This line intentionally tries to use the "normal" name,
            # which does not exist - only '__sensitive_data' does,
            # and Python has renamed that internally for us.
            return self.sensitive_data  # noqa: this is expected to fail
        except AttributeError:
            return (
                "Access denied: 'sensitive_data' is not directly accessible "
                "from outside the SecureEnclave class."
            )
