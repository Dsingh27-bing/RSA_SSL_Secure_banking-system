# client.py
import socket
import rsa
from cryptography.fernet import Fernet
import pickle
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket object
host_name = sys.argv[1]
port = int(sys.argv[2])
s.connect((host_name, port))  # connecting making, 1234- port number
full_msg = ''

while True:
    user_id = input("Enter your user id : ")

    password = input("Enter your password : ")

    sym_key = Fernet.generate_key()      #fernet is used for symmetric key used for encryption of user id password
    fernet = Fernet(sym_key)
# loading the public key from the public key .PEM file
    with open("public.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read()) #loading public key in public_key

# Encrypting the symmetric key with the public key
    encrypted_sym_key = rsa.encrypt(sym_key, public_key)   #encrypting fernet symmetric key and public key with rsa 

    encrypted_user_id = fernet.encrypt(user_id.encode())   #using fernet encryption of userid
    encrypted_password = fernet.encrypt(password.encode()) #using fernet encryption of password

    data = pickle.dumps([encrypted_sym_key, encrypted_user_id, encrypted_password]) #pickle sends data in list form
    s.send(data)
# while True:
    msg = s.recv(1024)  # receiving data
    # if len(msg) <= 0:
    #     break
    full_msg = msg.decode("utf-8")
    # print(full_msg)
    if full_msg == "1":
        while True:
            balance = s.recv(1024).decode("utf-8")
            choice = input(f"Your account balance is ${balance}.Please select one of the following actions:\n 1.Transfer\n 2.Exit\n")
            if choice == "1":
                trans_acc = input("Enter the account ID to which the money to be transferred: ")
                trans_amount = input("Enter the amount to be transferred: ")

                trans_data = pickle.dumps(["1",trans_acc, trans_amount])
                s.send(trans_data)

                ret_msg = s.recv(1024).decode("utf-8")
                if ret_msg == "1":
                    print("Your Transaction is successful")
                else:
                    print("Your Transaction is unsuccessful")
            else:
                s.send(pickle.dumps(["2"]))
                s.close()
                exit()




