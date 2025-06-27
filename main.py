from encryption_utils import *
from metadata_handler import *
import os

def cli():
    print("\n🔐 Secure File Storage System 🔐")
    print("1. Encrypt File")
    print("2. Decrypt File")
    choice = input("Enter option: ")

    if choice == "1":
        path = input("Enter file path to encrypt: ")
        if not os.path.exists(path):
            print("[!] File not found.")
            return

        try:
            key = load_key()
        except FileNotFoundError:
            print("[*] Generating new key...")
            key = generate_key()

        enc_path = encrypt_file(key, path)
        file_hash = get_sha256_hash(path)
        save_metadata(path, enc_path, file_hash)
        print(f"[+] Encrypted file saved as: {enc_path}")

    elif choice == "2":
        enc_path = input("Enter .enc file path to decrypt: ")
        if not os.path.exists(enc_path):
            print("[!] File not found.")
            return

        try:
            key = load_key()
        except FileNotFoundError:
            print("[!] Key not found. Cannot decrypt.")
            return

        item = find_metadata_by_encrypted(enc_path)
        if not item:
            print("[!] No metadata found for this file.")
            return

        dec_path = decrypt_file(key, enc_path)
        current_hash = get_sha256_hash(dec_path)

        if current_hash == item['hash']:
            print(f"[+] Decrypted file saved as: {dec_path}")
            print("[+] Integrity verified.")
        else:
            print("[!] Tampering detected or file mismatch!")

if __name__ == "__main__":
    cli()
