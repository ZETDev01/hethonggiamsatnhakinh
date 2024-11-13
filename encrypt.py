from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

# Define the AES key and IV
aes_key = bytes([0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, 0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C])
iv = bytes([0x00] * 16)  # Default IV of 16 bytes with all zeros

# Function to encrypt plaintext with AES-128-CBC
def encrypt_aes_cbc(plaintext):
    # Add PKCS7 padding to the plaintext
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    # Create a Cipher object with AES-128-CBC mode
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Encode the ciphertext as base64 for readability
    return base64.b64encode(ciphertext).decode('utf-8')

# Function to decrypt ciphertext with AES-128-CBC
def decrypt_aes_cbc(ciphertext):
    # Decode from base64
    ciphertext = base64.b64decode(ciphertext)

    # Create a Cipher object with AES-128-CBC mode
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode('utf-8')

# Example usage of encryption and decryption
plaintext = input("Enter plaintext to encrypt:\n")
encrypted = encrypt_aes_cbc(plaintext)
print("Encrypted (base64):", encrypted)

# Decrypt the encrypted text
decrypted = decrypt_aes_cbc(encrypted)
print("Decrypted text:", decrypted)
