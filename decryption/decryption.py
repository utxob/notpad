import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad

desktop_path = os.path.expanduser("~/Desktop")

# Load RSA Private Key from file
private_key_path = "private.pem"
with open(private_key_path, "rb") as key_file:
    private_key_data = key_file.read()
private_key = RSA.import_key(private_key_data)
cipher_rsa = PKCS1_OAEP.new(private_key)

def decrypt_file(file_path, cipher_rsa):
    try:
        with open(file_path, "rb") as f:
            iv = f.read(16)
            encrypted_aes_key = f.read(256)
            encrypted_data = f.read()
        
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)
        
        original_file_path = file_path.replace(".enc", "")
        with open(original_file_path, "wb") as f:
            f.write(decrypted_data)
        
        os.remove(file_path)
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

def decrypt_directory(directory, cipher_rsa):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".enc"):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, cipher_rsa)

print("YOUR file decryption Processing...")
decrypt_directory(desktop_path, cipher_rsa)
print("Decryption Complete! All files restored.")
