from cryptography.fernet import Fernet
from flask import current_app

def get_cipher_suite():
    """
    Creates a Fernet cipher suite instance using the secret key from the app config.
    The FERNET_KEY should be a URL-safe base64-encoded 32-byte key.
    """
    key = current_app.config.get('FERNET_KEY')
    if not key:
        raise ValueError("FERNET_KEY is not set in the application configuration. "
                         "Generate one using `cryptography.fernet.Fernet.generate_key()`.")
    return Fernet(key.encode())

def encrypt_data(data_str: str) -> str:
    """Encrypts a string and returns it as a string."""
    if not data_str:
        return None
    cipher_suite = get_cipher_suite()
    encrypted_bytes = cipher_suite.encrypt(data_str.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_data(encrypted_str: str) -> str:
    """Decrypts a string and returns it as a string."""
    if not encrypted_str:
        return None
    cipher_suite = get_cipher_suite()
    decrypted_bytes = cipher_suite.decrypt(encrypted_str.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')

# To generate a new key for your .env file, you can run:
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
