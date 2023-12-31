# coding: utf-8
# Project: dsl
# File: interpreter_server.py
# Author: 郭骐畅
# Date: 2023/12/2 20:30

from parsing.parser import *
from user import *
import time

import socket
import select


class Action:
    """

    """

    def __init__(self):
        self.script = []  # 脚本语言
        self.user = User()  # 当前用户
        self.step = []  # 当前执行步骤
        self.currentStep = []
        self.speak = ""
        self.stepId = 0
        self.stepDic = {}  # 基于脚本树能够生成的可供执行的步骤
        self.isOver = False  # 是否结束
        self.waitTime = 0  # wait的时间
        self.input = ""  # 用户的输入
        # self.stop = False
        self.isSpeakCorrect = False  # 用于判断用户的输入是否符合标准，符合时为True
        self.conn = None
        self.address = None

    def get_script(self, l: list):
        """
        获得对应的脚本语法树

        @param l:
        @return:
        """
        self.script = get_files(l)

    def initialize_step(self):
        """
        初始化步骤

        @return:
        """
        self.step = self.script[0]
        self.currentStep = list(self.step)

    def fill_stepDic(self):
        """
        填充步骤字典

        @return:
        """
        for item_dic in self.script:
            #  self.stepDic[self.stepId] = item_dic[1]
            self.stepDic[item_dic[1]] = self.stepId
            self.stepId += 1

    def execute_script(self):
        """

        @return:
        """
        self.step = list(self.currentStep)
        for item_dic in self.step[2:]:
            for item in item_dic:
                if item[0] == "Speak":
                    answer_dic = item[1]
                    for sentence in answer_dic:
                        if sentence.startswith('$'):
                            if sentence[1:] == "name":
                                self.speak = self.speak + self.user.name
                            elif sentence[1:] == "money":
                                self.speak = self.speak + str(self.user.balance)
                        elif sentence != '+':
                            self.speak = self.speak + sentence.strip('"')
                    self.conn.send(self.speak.encode())
                    self.speak = ""
                elif item[0] == "Wait":
                    self.waitTime = item[1]
                    # timer_thread = threading.Thread(target=self.timer)
                    # timer_thread.start()
                elif item[0] == "Branch":
                    if not self.input:
                        ready_to_read, _, _ = select.select([self.conn], [], [], self.waitTime)  # 10秒超时
                        if ready_to_read:
                            self.input = self.conn.recv(1024).decode()
                        else:
                            message = "等待时间过长，即将退出程序"
                            self.conn.send(message.encode())
                            time.sleep(0.1)  # 等待10秒后关闭连接
                            self.conn.close()
                            return
                    # print(item[1].split('"')[1])
                    if item[1].split('"')[1] == self.input:
                        self.isSpeakCorrect = True
                        self.stepID = self.stepDic[item[2][0]]
                        self.step = self.script[self.stepID]
                        self.currentStep = list(self.step)
                        self.input = ""
                        return
                elif item[0] == "Change":
                    answer = item[1]
                    if answer.startswith('$'):
                        if answer[1:] == "name":
                            ready_to_read, _, _ = select.select([self.conn], [], [], self.waitTime)  # 10秒超时
                            if ready_to_read:
                                self.user.name = self.conn.recv(1024).decode()
                        elif answer[1:] == "money":
                            if item[2] == "+":
                                ready_to_read, _, _ = select.select([self.conn], [], [], self.waitTime)  # 10秒超时
                                if ready_to_read:
                                    self.user.balance += int(self.conn.recv(1024).decode())
                            elif item[2] == '-':
                                self.user.balance -= item[3]
                elif item[0] == "Default":
                    if self.input != "退出" and self.input != "":
                        message = "您当前的输入不符合标准，将返回初始界面"
                        self.conn.send(message.encode())
                        time.sleep(1)
                        self.step = self.script[0]
                        self.currentStep = list(self.step)
                        self.input = ""
                        return
                elif item == 'Exit':
                    if not self.input:
                        ready_to_read, _, _ = select.select([self.conn], [], [], self.waitTime)  # 10秒超时
                        if ready_to_read:
                            self.input = self.conn.recv(1024).decode()
                        else:
                            message = "等待时间过长，即将退出程序"
                            self.conn.send(message.encode())
                            time.sleep(5)  # 等待10秒后关闭连接
                            self.conn.close()
                            return
                    if self.input == "退出":
                        self.isOver = True
                        print("客户已退出")
                        return
                    else:
                        message = "您当前的输入不符合标准，将返回初始界面"
                        self.conn.send(message.encode())
                        self.step = self.script[0]
                        self.currentStep = list(self.step)
                        self.input = ""
                        return


def interpreter(action: Action, file_list: list):
    """
    解释脚本语言，根据脚本生成树执行对应的动作

    @param action:
    @param file_list:
    @return:
    """
    action.get_script(file_list)
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
