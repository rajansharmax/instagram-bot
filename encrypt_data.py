import json
from cryptography.fernet import Fernet

# Function to generate a Fernet key for encryption/decryption
def generate_key():
    return Fernet.generate_key()

# Function to initialize a Fernet cipher with a given key
def initialize_cipher(key):
    return Fernet(key)

# Function to encrypt data using a Fernet cipher
def encrypt_data(cipher, data):
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data using a Fernet cipher
def decrypt_data(cipher, encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

# Generate a new encryption key
key = generate_key()
cipher = initialize_cipher(key)

def load_last_user_details():
    try:
        with open("last_user.json", "r") as f:
            data = json.load(f)
            return data.get("accounts", [])
    except FileNotFoundError:
        return []

accounts_data = load_last_user_details()
# Original data containing usernames and passwords

# Encrypt usernames and passwords
encrypted_accounts = []
for account in accounts_data:
    encrypted_username = encrypt_data(cipher, account['username'])
    encrypted_password = encrypt_data(cipher, account['password'])
    encrypted_accounts.append({
        "username": encrypted_username.decode(),
        "password": encrypted_password.decode()
    })

# Create a new dictionary with encrypted accounts
encrypted_data = {
    "accounts": encrypted_accounts
}

# Save encrypted data to a new encrypted file
encrypted_file_path = "encrypted_last_user.json"
with open(encrypted_file_path, "w") as f:
    json.dump(encrypted_data, f, indent=4)

access_key = "saved_media/key.json"
with open(access_key, "w") as f:
    json.dump(key.decode(), f, indent=4)

print(f"Encrypted usernames and passwords saved to: {encrypted_file_path}")
print(f"Encryption key (keep this secure): {key.decode()}")
