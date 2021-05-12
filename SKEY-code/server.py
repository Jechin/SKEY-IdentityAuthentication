#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
import os
import string
import random
import json
import hashlib
import datetime


class server:
    def __init__(self):
        self.sock_server = socket(AF_INET, SOCK_STREAM)
        address = ('', 8888)

        self.sock_server.bind(address)
        self.sock_server.listen(5)
        print("Server Starts!")

        self.f = open('user.txt', 'r+')
        self.log_file = open('log.txt', 'a')
        self.user = {}
        read = self.f.read()
        if read != "":
            self.user = json.loads(read)

    def start(self):
        self.sock_client, self.addr_client = \
        self.sock_server.accept()
        print("Accept from ", self.addr_client[0], 
            self.addr_client[1])
        while True:
            choice = self.recv_choice()
            print("choice: ", choice)
            if choice == 0:
                break
            elif choice == 1:
                self.register()
            elif choice == 2:
                self.login()

    def login(self):
        login_info = self.sock_client.recv(1024).decode()
        usrname = list(json.loads(login_info).keys())[0]
        passwd = list(json.loads(login_info).values())[0]
        if usrname in self.user:
            Skey = hashlib.md5(passwd.encode('UTF-8')).hexdigest()
            if Skey == self.user[usrname]:
                send_buff = "Login Successfully"
                self.sock_client.send(send_buff.encode('UTF-8'))
                self.user[usrname] = passwd
                self.f.seek(0)
                self.f.write(json.dumps(self.user))
                self.f.flush()
                self.log(self.addr_client, usrname, "login", "sucs")
                status = self.recv_status()
                if status == 0:
                    self.reseed()
                print(usrname + 
                    " login successfully status: ", status)
                return
        send_buff = "Login failed"
        self.log(self.addr_client, usrname, "login", "fail")
        self.sock_client.send(send_buff.encode('UTF-8'))

    def recv_status(self):
        status = self.sock_client.recv(1).decode('UTF-8')
        try:
            if 0 <= int(status) <= 8:
                return int(status)
            else:
                print("recv status error")
        except Exception:
            print("recv status error")

    def recv_choice(self):
        choice = self.sock_client.recv(1).decode('UTF-8')
        try:
            if 0 <= int(choice) <= 2:
                return int(choice)
            else:
                print("recv choice error")
        except Exception:
            print("recv choice error")

    def register(self):
        seed = ''.join(random.sample(string.ascii_letters + 
            string.digits, 20))
        self.sock_client.send(seed.encode('UTF-8'))
        data = self.sock_client.recv(1024).decode('UTF-8')
        if data == "" or data == "Cancel":
            return
        usrname = list(json.loads(data).keys())[0]
        passwd = list(json.loads(data).values())[0]
        if usrname not in self.user:
            self.user[usrname] = passwd
            self.f.seek(0)
            self.f.write(json.dumps(self.user))
            self.f.flush()
            send_buff = "Register Successfully"
            self.log(self.addr_client, usrname, "regst", "sucs")
        else:
            send_buff = "Username already exists, please try again"
        print(usrname + " " + send_buff)
        self.sock_client.send(send_buff.encode('UTF-8'))

    def log(self, addr, user, action, result):
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time, 
            '%Y-%m-%d %H:%M:%S ')
        log = time_str + addr[0] + " " + str(addr[1]) + " " + \
        user + " " + action + " " + result + '\n'
        self.log_file.write(log)
        self.log_file.flush()

    def reseed(self):
        seed = ''.join(random.sample(string.ascii_letters + \
            string.digits, 20))
        self.sock_client.send(seed.encode('UTF-8'))
        data = self.sock_client.recv(1024).decode('UTF-8')
        if data == "" or data == "Cancel":
            return
        usrname = list(json.loads(data).keys())[0]
        passwd = list(json.loads(data).values())[0]
        if usrname in self.user:
            self.user[usrname] = passwd
            self.f.seek(0)
            self.f.write(json.dumps(self.user))
            self.f.flush()
            send_buff = "Reseed Successfully"
        else:
            send_buff = "Reseed failed"
        print(send_buff)
        self.sock_client.send(send_buff.encode('UTF-8'))

    def __del__(self):
        self.sock_server.close()
        self.sock_client.close()
        self.f.close()
        self.log_file.close()


Server = server()
Server.start()
