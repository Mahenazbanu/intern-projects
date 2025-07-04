# **Technical Report: Secure File Encryption and Management Tool**

## **Project Title**  
**Secure File Encryption and Management Tool (AES-256)**

---

## **Objective / Purpose of the Tool**

This software tool is designed to securely encrypt and decrypt files using **AES-256 in CBC mode**, ensuring confidentiality and data integrity. It provides two user interfaces—**CLI and GUI**—for ease of use across different environments. Additionally, it stores metadata about encrypted files, including their original name, timestamp, and SHA-256 hash, enabling tamper detection upon decryption.

The primary purpose of this tool is to:

- Safeguard sensitive data through strong symmetric encryption.
- Allow users to easily encrypt and decrypt files via either command-line or graphical interface.
- Verify file integrity using cryptographic hashing.
- Maintain a database of encrypted file metadata for auditing and tracking purposes.

---

## **Key Features and Functionalities**

1. **AES-256 Encryption/Decryption**
   - Uses `cryptography` library for secure AES-256 CBC operations.
   - Random initialization vector (IV) for each encryption operation.
   - PKCS#7 padding implemented manually for block alignment.

2. **File Hashing (SHA-256)**
   - Computes SHA-256 hash of original files before encryption.
   - Validates file integrity after decryption by comparing stored and current hashes.

3. **Metadata Handling**
   - Stores metadata (original path, encrypted path, timestamp, hash) in a JSON file (`metadata.db`).
   - Allows lookup of metadata during decryption to verify file origin and integrity.

4. **User Interfaces**
   - **CLI Interface:** Simple menu-driven terminal interface.
   - **GUI Interface:** Qt-based desktop application with file dialogs and status feedback.

5. **Automatic Key Generation**
   - Generates and saves a 256-bit key if none exists.
   - Loads existing key from disk when available.

6. **Tamper Detection**
   - Compares decrypted file hash with original hash stored in metadata.
   - Alerts user if tampering or mismatch is detected.

---

## **Architecture Overview and Design Approach**

The system follows a **modular architecture**, separating concerns into distinct components:

### **High-Level Architecture Diagram**
```
+------------------+       +----------------------+       +--------------------+
|     User Input   | <-->  |    Core Logic        | <-->  |   Data Storage     |
| (CLI/GUI)        |       | (Encryption Utils)   |       | (Key, Metadata DB) |
+------------------+       +----------------------+       +--------------------+
```

### **Design Principles Applied**
- **Separation of Concerns**: Each module handles a specific responsibility (encryption, UI, metadata).
- **Security First**: Strong cryptographic primitives used throughout.
- **Simplicity and Usability**: Both CLI and GUI interfaces ensure accessibility.
- **Data Integrity Assurance**: Hash-based validation ensures authenticity.

---

## **Modules/Components Description**

### **1. `encryption_utils.py`**
**Purpose**: Provides core encryption, decryption, and hashing functions.

#### Functions:
- `generate_key()`: Creates and saves a random 256-bit AES key.
- `load_key()`: Reads the previously saved key from disk.
- `encrypt_file(key, in_path, out_path)`: Encrypts a file using AES-256-CBC.
- `decrypt_file(key, in_path, out_path)`: Decrypts a `.enc` file and removes padding.
- `get_sha256_hash(file_path)`: Computes and returns the SHA-256 hash of a file.

### **2. `gui.py`**
**Purpose**: Implements a PyQt5-based graphical interface for the tool.

#### Classes:
- `SecureFileManager(QWidget)`: Main GUI window with buttons for encryption and decryption.
  - Opens file dialogs.
  - Handles encryption and decryption logic using utility functions.
  - Displays status messages and integrity checks.

### **3. `main.py`**
**Purpose**: Command-line interface for interacting with the tool.

#### Functions:
- `cli()`: Presents a simple text menu for selecting encryption or decryption.
  - Accepts file paths from the user.
  - Invokes appropriate functions and displays results.

### **4. `metadata_handler.py`**
**Purpose**: Manages metadata storage and retrieval.

#### Functions:
- `save_metadata(original_path, encrypted_path, file_hash)`: Saves metadata to `metadata.db`.
- `find_metadata_by_encrypted(enc_path)`: Retrieves metadata for a given encrypted file.

---

## **Technology Stack Used**

| Layer             | Technology / Library                                                              |
|------------------|------------------------------------------------------------------------------------|
| Language          | Python 3.x                                                                        |
| Cryptography      | `cryptography` (hazmat backend), `hashlib`                                        |
| GUI               | PyQt5                                                                             |
| File Format       | Plaintext, Binary, JSON (.db)                                                     |
| OS Support        | Cross-platform (Windows, Linux, macOS)                                            |

---

## **Installation and Setup Instructions**

### **Prerequisites**
- Python 3.x installed
- pip package manager

### **Steps**
1. Clone or extract the project directory containing all four files.
2. Install dependencies:
   ```bash
   pip install cryptography PyQt5
   ```
3. Ensure all Python files are in the same working directory.

---

## **How to Use the Tool**

### **CLI Mode**
Run:
```bash
python main.py
```
Choose option 1 to encrypt or 2 to decrypt:
- Enter the file path.
- The tool will generate or load a key automatically.
- Encrypted files are saved with `.enc` extension.
- Decrypted files are saved with `_decrypted` suffix.

### **GUI Mode**
Run:
```bash
python gui.py
```
Click "Encrypt File" or "Decrypt File":
- Select files via dialog.
- Status updates shown in label.
- Tampering alerts displayed if detected.

---

## **Security and Performance Considerations**

### **Security**
- Uses **AES-256** with **CBC mode** for strong encryption.
- Manual **PKCS#7 padding** ensures correct block size.
- **SHA-256 hashing** ensures data integrity.
- **Random IVs** prevent pattern leakage.
- **Key stored locally** – must be protected physically or with access controls.

### **Performance**
- Efficient chunked reading for large files in hashing function.
- Encryption/decryption is fast due to hardware-accelerated AES instructions.
- Metadata handling uses lightweight JSON format.

---

## **Limitations and Known Issues**

1. **No Key Management System**
   - The secret key is stored in plaintext as `secret.key`. This could be a security risk if not properly secured.

2. **Single-user Assumption**
   - The tool assumes a single user and does not support multi-user access or role-based permissions.

3. **No Backup of Metadata**
   - If `metadata.db` is lost or corrupted, decryption cannot verify file integrity or origin.

4. **Lack of Unit Tests**
   - No automated tests included to validate correctness of encryption, decryption, or metadata handling.

5. **No Password-based Key Derivation**
   - Currently uses raw binary keys; no support for passphrase-based key generation (e.g., PBKDF2).

---

## **Future Improvements or Recommendations**

1. **Implement Key Management**
   - Add support for password-based key derivation using PBKDF2 or Argon2.
   - Allow export/import of keys with optional encryption.

2. **Add Multi-user Support**
   - Store per-user keys and metadata.
   - Implement access control policies.

3. **Enhance Metadata Management**
   - Use SQLite instead of JSON for better querying and scalability.
   - Add backup/export functionality for metadata.

4. **Add Logging and Error Reporting**
   - Log all operations with timestamps and user identifiers.
   - Provide detailed error messages for troubleshooting.

5. **Automated Testing**
   - Write unit tests for encryption, decryption, and metadata handling.
   - Integrate with CI/CD pipeline for regression testing.

6. **Cross-platform Packaging**
   - Package the GUI version as an executable (e.g., PyInstaller).
   - Distribute as a standalone app for non-developers.

7. **Support for Folders and Batch Processing**
   - Extend encryption/decryption to entire directories.
   - Add batch processing options in CLI and GUI.

---

## **Conclusion**

This Secure File Encryption and Management Tool offers robust AES-256 encryption and integrity verification using SHA-256. With both CLI and GUI interfaces, it caters to a wide range of users—from developers to general users. While currently suitable for basic use cases, enhancements in key management, metadata resilience, and usability would make it production-ready for enterprise applications.

The modular design allows for easy maintenance and future expansion, making it a solid foundation for secure file handling systems.

---

## **Author:** Mahenazbanu
