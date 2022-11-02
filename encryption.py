from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_key():
    return rsa.generate_private_key(public_exponent=65537,key_size=4096)
# Generate the RSA private key

def get_public_key(key) -> bytes:
    return key.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

def encrypt_data(data:bytes, key):
    key = serialization.load_pem_public_key(key)
    encrypted_data =  key.encrypt(
    data,padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
    return encrypted_data

def decrypt_data(data:bytes, key):
    decrypted_data = key.decrypt(
    data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
    return decrypted_data

def main():
    key = generate_key()
    public_key = get_public_key(key)
    # print(len(public_key))
    encrypted_data = encrypt_data(b'secret secret ',public_key)
    print(len(encrypted_data))
    decrypted_data = decrypt_data(encrypted_data, key)
    print(len(decrypted_data))

if __name__ == "__main__":
    main()
    
