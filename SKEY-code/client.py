#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
import random
import getpass
import json
import hashlib


class client:
    def __init__(self):
        self.sock_client = socket(AF_INET, SOCK_STREAM)
        address = ('127.0.0.1', 8888)
        self.sock_client.connect(address)
        print("Connect Server Successfully!")

        self.f = open('login.txt', 'r+')
        read = self.f.read()
        self.user = dict()
        if read != "":
            self.user = json.loads(read)

    def start(self):
        while True:
            self.choice = self.menu()
            if self.choice == 1:
                self.register()
            elif self.choice == 2:
                self.login()
            elif self.choice == 0:
                break

    def menu(self):
        print("\n")
        print("----menu----")
        print("1. register")
        print("2. login")
        print("0. exit")
        while True:
            choice = input("choice: ")
            try:
                if int(choice) == 0 or int(choice) == 1 \
                or int(choice) == 2:
                    self.sock_client.send(choice.encode('UTF-8'))
                    return int(choice)
                else:
                    print("Invalid choice: ", choice)
                    continue
            except Exception:
                print("Invalid choice: ", choice)
                continue

    def login(self):
        usrname = input("input your usrname: ")
        passwd = getpass.getpass("Input your password: ")
        if usrname not in self.user:
            print("User does not exist")
            return
        while(1):
            if self.certificate() == 1:
                break;
        status = self.user[usrname]
        if status[1] != 0:
            Skey = self.skey(status[0], status[1] - 1, passwd)
            send_buff = json.dumps({usrname: Skey})
            self.sock_client.send(send_buff.encode('UTF-8'))
            answer = self.recv_answer()
            if answer == "Login Successfully":
                print(usrname + " " + answer)
                status[1] = int(status[1]) - 1
                self.user[usrname] = status
                self.f.seek(0)
                self.f.write(json.dumps(self.user))
                self.f.flush()
                self.send_status(status[1])
                while status[1] == 0:
                    temp = self.reseed(usrname, passwd)
                    if temp[1] == 8:
                        status = temp
                self.user[usrname] = status
                self.f.seek(0)
                self.f.write(json.dumps(self.user))
                self.f.flush()

    def reseed(self, usrname, passwd):
        seed = self.recv_seed()
        Skey = self.skey(seed, 8, passwd)
        send_buff = json.dumps({usrname: Skey})
        self.sock_client.send(send_buff.encode('UTF-8'))
        answer = self.recv_answer()
        if answer == "Reseed Successfully":
            status = [seed, 8]
            return status
        elif answer == "Reseed failed":
            status = [seed, 0]
            return status
        else:
            print(answer)
            status = [seed, 0]
            return status

    def register(self):
        seed = self.recv_seed()
        usrname = input("input your usrname: ")
        passwd = getpass.getpass("Input your password: ")
        confirm = getpass.getpass("Confirm your password: ")
        if passwd == confirm:
            Skey = self.skey(seed, 8, passwd)
            send_buff = json.dumps({usrname: Skey})
            self.sock_client.send(send_buff.encode('UTF-8'))
        else:
            send_buff = "Cancel"
            self.sock_client.send(send_buff.encode('UTF-8'))
            print("Inconsistent passwords")
        answer = self.recv_answer()
        if answer == "Register Successfully":
            status = [seed, 8]
            self.user[usrname] = status
            self.f.seek(0)
            self.f.write(json.dumps(self.user))
            self.f.flush()

    def send_status(self, status):
        self.sock_client.send(str(status).encode('UTF-8'))

    def recv_answer(self):
        data = self.sock_client.recv(1024).decode('UTF-8')
        print(data)
        return data

    def recv_seed(self):
        seed = self.sock_client.recv(20).decode('UTF-8')
        print(seed)
        return seed

    def skey(self, seed, n, passwd):
        temp = seed + passwd
        MD = hashlib.md5(temp.encode('UTF-8')).hexdigest()
        left = MD[0:16]
        right = MD[16:32]
        Skey = ''
        for i in range(16):
            Skey = Skey + hex(int(left[i], 16) 
                ^ int(right[i], 16))[2:]
        for i in range(n):
            Skey = hashlib.md5(Skey.encode('UTF-8')).hexdigest()

        return Skey

    def certificate(self):
        code = random.randint(1000, 9999)
        print("Code: ", code)
        input_code = int(input("Input Verification Code："))
        if input_code != code:
            return 0
        else:
            return 1

    def __del__(self):
        print("Disconnect with Server!")
        self.sock_client.close()
        self.f.close()


Client = client()
Client.start()
