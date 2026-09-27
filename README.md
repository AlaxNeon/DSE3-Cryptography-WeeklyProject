# Cryptography Weekly Projects

A collection of weekly cryptography projects implemented in Python as part of a learning journey into modern cryptography, embedded security, confidential computing, and post-quantum cryptography.

Each week is maintained in its own folder and contains its own `README.md` with detailed implementation, execution steps, tests, and learning outcomes.

---

## 📚 Weekly Projects

| Week | Topic | Folder | Description |
|---|---|---|---|
| **Week 1** | **ChaCha20-Poly1305 AEAD** | [`Week-1`](./Week-1/) | Demonstrates authenticated encryption using ChaCha20-Poly1305, including encryption, decryption, AAD, and tamper detection. |
| **Week 2** | **Secure Enclave / Intel SGX** | [`Week-2`](./Week-2/) | Demonstrates confidential in-memory computation using a Python simulation of the Intel SGX enclave concept. |
| **Week 3** | **Post-Quantum Falcon Signatures** | [`Week-3`](./Week-3/) | Demonstrates post-quantum digital-signature concepts, Falcon at a high level, lattice cryptography, FFT, signature verification, and tamper detection. |

---

## 🗂️ Repository Structure

```text
Cryptography/
│
├── README.md
│
├── Week-1/
│   ├── README.md
│   ├── main.py
│   ├── chacha20_poly1305.py
│   ├── test_chacha20_poly1305.py
│   ├── requirements.txt
│   └── ...
│
├── Week-2/
│   ├── README.md
│   ├── main.py
│   ├── secure_enclave.py
│   ├── test_secure_enclave.py
│   ├── requirements.txt
│   └── ...
│
└── Week-3/
    ├── README.md
    ├── main.py
    ├── falcon_demo.py
    ├── fft_demo.py
    ├── test_falcon_demo.py
    ├── requirements.txt
    └── ...
```

---

# 🔐 Week 1 — ChaCha20-Poly1305 AEAD

### Objective

Implement and demonstrate **ChaCha20-Poly1305 Authenticated Encryption with Associated Data (AEAD)** using Python.

The project demonstrates:

- 256-bit key generation
- Secure nonce generation
- Encryption
- Decryption
- Authentication
- Additional Authenticated Data (AAD)
- Ciphertext tamper detection
- Authentication failure handling

### Main Concept

```text
Plaintext
    │
    ▼
ChaCha20-Poly1305
    │
    ├── Ciphertext
    ├── Authentication Tag
    └── Nonce
    │
    ▼
Encrypted IoT Data
    │
    ▼
ChaCha20-Poly1305
    │
    ▼
Original Plaintext
```

### Run Week 1

```bash
cd Week-1

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

Run tests:

```bash
python -m unittest test_chacha20_poly1305.py
```

📖 **Detailed documentation:** [`Week-1/README.md`](./Week-1/README.md)

---

# 🛡️ Week 2 — Secure Enclave / Intel SGX

### Objective

Demonstrate the concept of **confidential in-memory computation** using a simple Python simulation of an Intel SGX-style secure enclave.

The project demonstrates:

- Secure enclave concepts
- Confidential computation
- Sensitive data isolation
- In-memory computation
- SHA-256 integrity verification
- Tamper detection
- Difference between a software simulation and real hardware-backed SGX

### Main Concept

```text
             Normal Application
                    │
                    │ Sensitive Data
                    ▼
          ┌─────────────────────┐
          │  Simulated Enclave  │
          │                     │
          │  Sensitive Data     │
          │        ↓            │
          │  Integrity Check    │
          │        ↓            │
          │  Computation        │
          └──────────┬──────────┘
                     │
                     │ Result Only
                     ▼
              Normal Application
```

### Important Note

The Week-2 implementation is an **educational Python simulation**.

It does **not** provide:

- CPU-enforced SGX isolation
- Hardware-protected enclave memory
- Real Intel SGX security guarantees

It is intended to explain the programming model and concepts before studying a genuine SGX implementation.

### Run Week 2

```bash
cd Week-2

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies if required:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

Run tests:

```bash
python -m unittest test_secure_enclave.py
```

📖 **Detailed documentation:** [`Week-2/README.md`](./Week-2/README.md)

---

# ⚛️ Week 3 — Post-Quantum Falcon Signature Scheme

### Objective

Explore the concept of **post-quantum digital signatures**, with a focus on Falcon, lattice cryptography, and FFT-based computations.

The project demonstrates:

- Digital signatures
- Public/private key concepts
- Message hashing
- Signature generation
- Signature verification
- Message tampering detection
- Post-quantum cryptography concepts
- Lattice cryptography concepts
- Fast Fourier Transform (FFT)
- Falcon's high-level relationship with FFT-based computation

### Main Concept

```text
                SIGNING

Message
   │
   ▼
 Hash
   │
   ▼
Private Key
   │
   ▼
Digital Signature
```

```text
              VERIFICATION

Message + Signature + Public Key
                │
                ▼
          Verification
                │
         ┌──────┴──────┐
         ▼             ▼
       VALID         INVALID
```

### FFT Concept

The project also contains a simple FFT demonstration:

```text
Time-Domain Signal
        │
        ▼
       FFT
        │
        ▼
Frequency-Domain Representation
```

### Important Note

Falcon is a sophisticated cryptographic algorithm. A simple Python educational project should **not** claim to be a production implementation of Falcon unless it uses a genuine, established Falcon implementation.

If the Week-3 project uses a conceptual simulation, it should be clearly labeled as an educational simulation and should not be used for real security.

### Run Week 3

```bash
cd Week-3

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

Run tests:

```bash
python -m unittest test_falcon_demo.py
```

📖 **Detailed documentation:** [`Week-3/README.md`](./Week-3/README.md)

---

# 🧭 Learning Roadmap

The weekly projects are designed to progressively explore different areas of modern cryptography.

```text
┌─────────────────────────────────────────────┐
│                  WEEK 1                     │
│                                             │
│          ChaCha20-Poly1305 AEAD             │
│                                             │
│   Confidentiality + Authentication          │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                  WEEK 2                     │
│                                             │
│       Confidential Computing / SGX          │
│                                             │
│      Protected Computation Concepts         │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                  WEEK 3                     │
│                                             │
│       Post-Quantum Cryptography             │
│              Falcon / Lattices              │
│                                             │
│       Digital Signatures + FFT              │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│               FUTURE WORK                   │
│                                             │
│        Post-Quantum IoT Security             │
│                                             │
│   Embedded Devices + Secure Communication   │
└─────────────────────────────────────────────┘
```

---

# 🎯 Overall Learning Goals

Through these projects, the main goals are to understand:

- Symmetric authenticated encryption
- Data confidentiality
- Data integrity
- Authentication
- Secure handling of IoT data
- Confidential computing
- Secure enclave concepts
- Hardware-backed security concepts
- Digital signatures
- Post-quantum cryptography
- Lattice-based cryptography
- FFT-based mathematical computation
- Cryptographic tamper detection
- Security considerations for embedded and IoT systems

---

# 🧪 Testing

Each weekly project contains its own test file.

Run the tests from the corresponding week directory.

### Week 1

```bash
python -m unittest test_chacha20_poly1305.py
```

### Week 2

```bash
python -m unittest test_secure_enclave.py
```

### Week 3

```bash
python -m unittest test_falcon_demo.py
```

---

# ⚠️ Educational Use

These projects are primarily intended for **learning and experimentation**.

Cryptographic software should not be considered secure for production merely because the demonstration works.

In particular:

- Do not use educational cryptographic implementations to protect real secrets.
- Do not hard-code production encryption keys.
- Do not reuse cryptographic nonces incorrectly.
- Do not treat Python encapsulation as a hardware security boundary.
- Do not treat toy post-quantum demonstrations as production cryptography.
- Use established, reviewed cryptographic libraries for real applications.

---

# 🚀 Future Direction

The long-term goal is to connect these concepts to **embedded and IoT security**.

Possible future projects include:

```text
ChaCha20-Poly1305
        │
        ▼
Secure Enclave / Confidential Computing
        │
        ▼
Post-Quantum Cryptography
        │
        ▼
Post-Quantum IoT Communication
        │
        ▼
Secure Firmware / Device Authentication
        │
        ▼
Embedded Security Prototype
```

---

## 👨‍💻 Author

**Somnath Gorai**

BCA — Internet of Things (IoT)

This repository contains weekly cryptography projects developed for academic learning and experimentation.

---

## 📌 Quick Navigation

- 📁 [Week 1 — ChaCha20-Poly1305 AEAD](./Week-1/)
- 📁 [Week 2 — Secure Enclave / Intel SGX](./Week-2/)
- 📁 [Week 3 — Post-Quantum Falcon](./Week-3/)
