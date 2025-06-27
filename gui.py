from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from encryption_utils import encrypt_file, decrypt_file, get_sha256_hash, load_key
from metadata_handler import save_metadata, find_metadata_by_encrypted
import os

class SecureFileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES Secure File Manager")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Select a file to encrypt or decrypt")
        layout.addWidget(self.label)

        self.enc_btn = QPushButton("Encrypt File", self)
        self.enc_btn.clicked.connect(self.encrypt_file_dialog)
        layout.addWidget(self.enc_btn)

        self.dec_btn = QPushButton("Decrypt File", self)
        self.dec_btn.clicked.connect(self.decrypt_file_dialog)
        layout.addWidget(self.dec_btn)

        self.setLayout(layout)

    def encrypt_file_dialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        if fname:
            try:
                key = load_key()
            except FileNotFoundError:
                key = os.urandom(32)
                with open("secret.key", "wb") as f:
                    f.write(key)

            enc_path = encrypt_file(key, fname)
            file_hash = get_sha256_hash(fname)
            save_metadata(fname, enc_path, file_hash)
            self.label.setText(f"Encrypted: {enc_path}")

    def decrypt_file_dialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select .enc File to Decrypt")
        if fname:
            try:
                key = load_key()
            except FileNotFoundError:
                self.label.setText("[!] Key not found. Cannot decrypt.")
                return

            item = find_metadata_by_encrypted(fname)
            if not item:
                self.label.setText("[!] No metadata found for this file.")
                return

            dec_path = decrypt_file(key, fname)
            current_hash = get_sha256_hash(dec_path)

            if current_hash == item['hash']:
                self.label.setText(f"Decrypted: {dec_path}\nIntegrity OK!")
            else:
                self.label.setText("[!] Tampering detected.")

if __name__ == "__main__":
    app = QApplication([])
    window = SecureFileManager()
    window.show()
    app.exec_()
