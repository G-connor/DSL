# coding: utf-8
# Project: dsl
# File: client.py
# Author: 郭骐畅
# Date: 2023/12/2 19:44

import socket
import threading


def receive_messages(client_socket,isConnect):
    while True:
        try:
            response = client_socket.recv(1024).decode()
            if not response:
                break  # 如果没有收到响应，则退出循环
            print(response)
            if response == "等待时间过长，即将退出程序":
                client_socket.close()
                isConnect = False
                break
        except Exception as e:
            print("连接已断开")
            break


def client_program():
    host = socket.gethostname()
    port = 12345

    client_socket = socket.socket()
    client_socket.connect((host, port))
    isConnect = True
    # 创建并启动接收消息的线程
    threading.Thread(target=receive_messages, args=(client_socket,isConnect)).start()

    while True:
        if isConnect:
            message = input("")
            if message.lower().strip() == "退出":
                break  # 如果输入"退出"，则关闭客户端
            client_socket.send(message.encode())
        else:
            break

    client_socket.close()


if __name__ == '__main__':
    client_program()
