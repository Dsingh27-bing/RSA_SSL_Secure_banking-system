# server.py
import socket
import pickle
import rsa
import hashlib
from cryptography.fernet import Fernet
import csv
import sys

port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket object
s.bind((socket.gethostname(), port))  # 1234 is the port number
s.listen(5)  # queue of 5 compatible with heavy load



# client_socket.send(bytes("Welcome to the server!", "utf-8"))  # sending info to client , type of bytes is utf-8
while True:
    client_socket, address = s.accept()  # accept client connections
    print(f"Connection from {address} has been established!!!")
    while True:
        recd_data1 = client_socket.recv(1024)       # for receiving id and password
        recd_data = pickle.loads(recd_data1) #pickle receives data in list from
        with open("private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read()) #loading private key in private_key

        sym_key = rsa.decrypt(recd_data[0], private_key) #decryption of sym key with private key
        fernet = Fernet(sym_key)
        user_id = fernet.decrypt(recd_data[1]).decode() #for user id 
        password = fernet.decrypt(recd_data[2]).decode() #for password

        hash_pass = hashlib.md5(password.encode()) #hash coding of password

        hash_pass_hex = hash_pass.hexdigest() #converting in hexadecimal form
        dict_pass = {} # creating a dictionary for userid and password
        with open("passwd.csv", newline='') as text:
            csv_read = csv.reader(text)
            batch_data = list(csv_read)
        for pair in batch_data:
            dict_pass[pair[0]] = pair[1]  #0th element is ids = keys(dictionary) and 1st element is password = value(dictionary) 

        if user_id in dict_pass.keys():
            if dict_pass[user_id] == hash_pass_hex:
                client_socket.send("1".encode())
                while True:
                    dict_pass1 = {} # dictionary for userid and balance 
                    with open("balance.csv", newline='') as text1:
                        csv_read1 = csv.reader(text1)
                        batch_data1 = list(csv_read1)
                    for pair in batch_data1:
                        dict_pass1[pair[0]] = pair[1]
                    client_socket.send(dict_pass1[user_id].encode())

                    trans_data1 = client_socket.recv(1024) # if client chooses 2 option of exit then break
                    trans_data = pickle.loads(trans_data1)
    # code for transfer amount from user's account to other's account
                    if trans_data[0] == "1":
                        if trans_data[1] in dict_pass1.keys():
                            if int(trans_data[2]) <= int(dict_pass1[user_id]):
                                temp_amount = int(trans_data[2])
                                dict_pass1[trans_data[1]] = str(int(dict_pass1[trans_data[1]])+ temp_amount)
                                dict_pass1[user_id] = str(int(dict_pass1[user_id]) - temp_amount)
                                with open("balance.csv", 'w', newline='') as csv_file:
                                    writer = csv.writer(csv_file)
                                    for key, value in dict_pass1.items():
                                        writer.writerow([key, value])
                                client_socket.send("1".encode())
                            else:
                                client_socket.send("0".encode())
                        else:
                            client_socket.send("0".encode())
                    else:
                        client_socket.close()
                        break
                break
            else:
                client_socket.send("0".encode())
        else:
            client_socket.send("0".encode())
