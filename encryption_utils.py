from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib

def generate_key():
    key = os.urandom(32)  # AES-256 key
    with open("secret.key", "wb") as f:
        f.write(key)
    return key

def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(key, in_path, out_path=None):
    if not out_path:
        out_path = in_path + ".enc"

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(in_path, 'rb') as f:
        plaintext = f.read()

    padding_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_len]) * padding_len

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(out_path, 'wb') as f:
        f.write(iv + ciphertext)

    return out_path

def decrypt_file(key, in_path, out_path=None):
    if not out_path:
        out_path = in_path.replace(".enc", "_decrypted")

    with open(in_path, 'rb') as f:
        data = f.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    padding_len = padded_data[-1]
    plaintext = padded_data[:-padding_len]

    with open(out_path, 'wb') as f:
        f.write(plaintext)

    return out_path

def get_sha256_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()
