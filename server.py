# coding: utf-8
# Project: dsl
# File: server.py
# Author: 郭骐畅
# Date: 2023/12/2 19:44

import socket
import select
import time  # 导入time模块
from interpreter.interpreter_server import *


def server_program():
    host = socket.gethostname()
    port = 12345

    files = ['D:/python project/dsl/example3.txt']
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("等待客户端连接")
    action = Action()
    conn, address = server_socket.accept()
    print("与" + str(address) + "连接成功")
    action.conn = conn
    action.address = address
    action.get_script(files)
    action.user.login()

    action.fill_stepDic()
    action.initialize_step()
    while True:
        action.execute_script()
        if action.isOver:
            break
        time.sleep(0.1)
    message = "您已退出程序，欢迎下次光临"
    action.conn.send(message.encode())
    # ready_sockets, _, _ = select.select([conn], [], [], 10)  # 10秒超时
    #
    # if ready_sockets:
    #     data = conn.recv(1024).decode()
    #     if data:
    #         print("Received from client: " + data)
    #     else:
    #         print("No data received")
    # else:
    #     print("Timeout reached, sending timeout message to client.")
    #     conn.sendall("Timeout reached. Closing connection.".encode())
    #     time.sleep(10)  # 等待1秒后关闭连接
    #     conn.close()

    server_socket.close()


if __name__ == '__main__':
    server_program()
