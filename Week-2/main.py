"""
main.py

Week-2: Secure Enclave (Intel SGX) Simulation for Confidential
In-Memory Computation.

Running this file will automatically run through the full
demonstration, step by step, and print clear output explaining what
is happening at each stage.

IMPORTANT: This program is an educational SIMULATION of the Intel SGX
programming model. It does NOT create a real hardware-backed SGX
enclave. See README.md for full details.
"""

from secure_enclave import SecureEnclave


def print_header(title):
    print("=" * 50)
    print(title)
    print("=" * 50)


def print_step(step_number, description):
    print(f"\n[{step_number}] {description}")


def main():
    print_header("Week-2: Secure Enclave Confidential Computation")

    print("\nNOTE:")
    print("This is a Python simulation of Intel SGX.")
    print("It is NOT a real hardware-backed SGX enclave.")

    # ------------------------------------------------------------
    # Step 1: Create the simulated enclave
    # ------------------------------------------------------------
    print_step(1, "Creating simulated secure enclave...")
    enclave = SecureEnclave()
    print("Enclave created successfully.")

    # ------------------------------------------------------------
    # Step 2: Load sensitive IoT sensor data
    # ------------------------------------------------------------
    print_step(2, "Loading sensitive IoT sensor data...")

    # Example IoT sensor readings (temperature, in Celsius).
    temperature_readings = [28.5, 29.1, 27.8, 30.2, 28.9]

    enclave.load_data(temperature_readings)
    print("\nSensitive data loaded into enclave.")

    # ------------------------------------------------------------
    # Step 3: Generate an integrity hash
    # ------------------------------------------------------------
    print_step(3, "Generating integrity hash...")
    print("SHA-256 integrity measurement created.")

    # ------------------------------------------------------------
    # Step 4: Perform confidential computation inside the enclave
    # ------------------------------------------------------------
    print_step(4, "Performing confidential computation...")
    print("\nComputation performed inside simulated enclave.")

    average_temp = enclave.compute_average()
    min_temp = enclave.compute_minimum()
    max_temp = enclave.compute_maximum()

    # ------------------------------------------------------------
    # Step 5: Return only the computation result
    # ------------------------------------------------------------
    print_step(5, "Result returned to application:")
    print(f"\nAverage Temperature: {average_temp:.2f} C")
    print(f"Minimum Temperature: {min_temp:.2f} C")
    print(f"Maximum Temperature: {max_temp:.2f} C")

    # ------------------------------------------------------------
    # Step 6: Demonstrate that direct access to internal data fails
    # ------------------------------------------------------------
    print_step(6, "Testing data isolation...")
    access_result = enclave.attempt_direct_access()
    print(f"\n{access_result}")
    print("Application cannot directly access enclave's sensitive data.")

    # ------------------------------------------------------------
    # Step 7: Verify integrity (should succeed - nothing changed yet)
    # ------------------------------------------------------------
    print_step(7, "Verifying integrity...")
    if enclave.verify_integrity():
        print("\nIntegrity verification successful.")
    else:
        print("\nIntegrity verification FAILED!")
        print("Sensitive data may have been modified.")

    # ------------------------------------------------------------
    # Step 8: Tampering demonstration
    # ------------------------------------------------------------
    print_step(8, "Tampering demonstration...")
    print("\nModifying sensitive data...")

    # Simulate an attacker or bug changing a value behind the
    # enclave's back (bypassing the normal load_data() method).
    enclave.simulate_external_tampering(index=2, new_value=97.8)

    if enclave.verify_integrity():
        print("\nIntegrity verification successful.")
    else:
        print("\nIntegrity verification FAILED!")
        print("Data modification detected.")

    print()
    print_header("Week-2 demonstration completed.")


if __name__ == "__main__":
    main()
