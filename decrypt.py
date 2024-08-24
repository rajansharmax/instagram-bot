import json
import os
from cryptography.fernet import Fernet

def initialize_cipher(key):
    return Fernet(key)

def decrypt_data(cipher, encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
    return decrypted_data

def load_keyfrom_file():
    try:
        key_file_path = "saved_media/videos/key.json"
        print(f"Attempting to open key file at: {key_file_path}")
        with open(key_file_path, "r") as f:
            key = f.read().strip()  # Read the key as a string
            print(f"Loaded key: {key}")  # Debugging output
            return key
    except FileNotFoundError:
        print(f"Key file not found at: {key_file_path}")
        return None

key = load_keyfrom_file()
if key is None:
    raise ValueError("Key is not available. Ensure the key file exists and contains a valid key.")

# Initialize Fernet cipher with the key
cipher = initialize_cipher(key)

encrypted_file_path = "encrypted_last_user.json"

try:
    with open(encrypted_file_path, "r") as f:
        encrypted_data = json.load(f)
        encrypted_accounts = encrypted_data.get("accounts", [])

    decrypted_accounts = []
    for account in encrypted_accounts:
        decrypted_username = decrypt_data(cipher, account["username"])
        decrypted_password = decrypt_data(cipher, account["password"])
        decrypted_accounts.append({
            "username": decrypted_username,
            "password": decrypted_password
        })

    print("Decrypted usernames and passwords:")
    for account in decrypted_accounts:
        print(f"Username: {account['username']}, Password: {account['password']}")

    output_file = "last_user.json"
    with open(output_file, "w") as f:
        json.dump({"accounts": decrypted_accounts}, f, indent=4)

except FileNotFoundError:
    print(f"File '{encrypted_file_path}' not found.")
except Exception as e:
    print(f"An error occurred while decrypting data: {str(e)}")
