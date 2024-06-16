import rsa
import secrets
import scrypt
import string
import random


# creating a symmetric key sym_key
random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
salt = secrets.token_bytes(32)
sym_key = scrypt.hash(random_string, salt, N=2048, r=8, p=1, buflen=32)

print("Symmetric key:", sym_key)
# loading the public key from the public key .PEM file
with open("public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Encrypting the symmetric key with the public key
encrypted_sym_key = rsa.encrypt(sym_key, public_key)
print("Encrypted Symmetric key : ", encrypted_sym_key)

with open("private.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

decrypted_sym_key = rsa.decrypt(encrypted_sym_key, private_key)

print("Decrypted symmetric key : ", decrypted_sym_key)



#
public_key, private_key = rsa.newkeys(1024)

with open("public.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

with open("private.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))
