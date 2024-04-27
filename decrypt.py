import json
from cryptography.fernet import Fernet

# Function to initialize a Fernet cipher with a given key
def initialize_cipher(key):
    return Fernet(key)

# Function to decrypt data using a Fernet cipher
def decrypt_data(cipher, encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
    return decrypted_data

def load_keyfrom_file():
    try:
        with open("saved_media/key.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []

# print("Decryption Script" + load_keyfrom_file())
# Load encryption key from a secure location (keep this secure)
key = load_keyfrom_file()

# Initialize a Fernet cipher with the encryption key
cipher = initialize_cipher(key)

# Path to the JSON file containing encrypted usernames and passwords
encrypted_file_path = "encrypted_last_user.json"

try:
    # Open the encrypted JSON file and load the data
    with open(encrypted_file_path, "r") as f:
        encrypted_data = json.load(f)
        encrypted_accounts = encrypted_data.get("accounts", [])

    # Decrypt usernames and passwords
    decrypted_accounts = []
    for account in encrypted_accounts:
        decrypted_username = decrypt_data(cipher, account["username"])
        decrypted_password = decrypt_data(cipher, account["password"])
        decrypted_accounts.append({
            "username": decrypted_username,
            "password": decrypted_password
        })

    # Display decrypted usernames and passwords
    print("Decrypted usernames and passwords:")
    for account in decrypted_accounts:
        print(f"Username: {account['username']}, Password: {account['password']}")

    # Path to the output JSON file
    output_file = "last_user.json"

    # Write user data to the JSON file
    with open(output_file, "w") as f:
        json.dump({"accounts": decrypted_accounts}, f, indent=4)

except FileNotFoundError:
    print(f"File '{encrypted_file_path}' not found.")
except Exception as e:
    print(f"An error occurred while decrypting data: {str(e)}")
