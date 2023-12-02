# coding: utf-8
# Project: dsl
# File: client.py
# Author: 郭骐畅
# Date: 2023/12/2 19:44

import socket


def client_program():
    host = socket.gethostname()
    port = 12345

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # message = input("请输入: ")
    # client_socket.send(message.encode())
    #
    # # 接收服务端的响应
    # response = client_socket.recv(1024).decode()
    # print("", response)
    while True:
        response = client_socket.recv(1024).decode()
        print(response)
        if response != "您当前的输入不符合标准，将返回初始界面":
            message = input("输入：")
            client_socket.send(message.encode())
            if message == "退出":
                break

    response = client_socket.recv(1024).decode()
    print(response)
    client_socket.close()


if __name__ == '__main__':
    client_program()
