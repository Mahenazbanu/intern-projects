import json
from datetime import datetime

def save_metadata(original_path, encrypted_path, file_hash):
    meta = {
        "original_name": original_path,
        "encrypted_name": encrypted_path,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hash": file_hash
    }

    try:
        with open("metadata.db", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"files": []}

    data["files"].append(meta)

    with open("metadata.db", "w") as f:
        json.dump(data, f, indent=4)

def find_metadata_by_encrypted(enc_path):
    try:
        with open("metadata.db", "r") as f:
            data = json.load(f)
        for item in data.get("files", []):
            if item["encrypted_name"] == enc_path:
                return item
        return None
    except Exception as e:
        print("[!] Error reading metadata:", str(e))
        return None
