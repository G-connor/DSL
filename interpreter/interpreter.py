# coding: utf-8
# Project: dsl
# File: interpreter.py
# Author: 郭骐畅
# Date: 2023/11/27 21:37

from parsing.parser import *
from user import *
import time
import threading
import sys
import queue

stop_loop = False


class Action:
    """

    """

    def __init__(self):
        self.script = []  # 脚本语言
        self.user = User()  # 当前用户
        self.step = []  # 当前执行步骤
        self.speak = ""
        self.stepId = 0
        self.stepDic = {}  # 基于脚本树能够生成的可供执行的步骤
        self.isTimeout = False  # 是否超时
        self.startTime = None  # 开始时间，用于计算总时间
        self.waitTime = 0  # wait的时间
        self.input = ""  # 用户的输入
        self.stop = False

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

    def fill_stepDic(self):
        """
        填充步骤字典

        @return:
        """
        for item_dic in self.script:
            #  self.stepDic[self.stepId] = item_dic[1]
            self.stepDic[item_dic[1]] = self.stepId
            self.stepId += 1

    def timer(self):
        """
        用于计时

        @return:
        """
        time.sleep(self.waitTime)
        self.isTimeout = True

    def input_with_timeout(self):
        """
        获取用户输入，如果在超时时间内未输入，则返回 None

        @return:
        """
        input_queue = queue.Queue()

        def get_input():
            try:
                input_queue.put(input())
            except:
                pass  # 可能需要处理特定的异常

        input_thread = threading.Thread(target=get_input)
        input_thread.daemon = True
        input_thread.start()

        while not input_thread.is_alive():
            if self.isTimeout:
                return None
            time.sleep(0.1)  # 稍微等待一下，避免过于频繁的检查

        input_thread.join()  # 等待用户输入线程结束
        if not self.isTimeout:
            return input_queue.get()
        else:
            return None

    def execute_script(self):
        for item_dic in self.step[2:]:
            for item in item_dic:
                if item[0] == "Speak":
                    answer_dic = item[1]
                    for sentence in answer_dic:
                        if sentence.startswith('$'):
                            if sentence[1:] == "name":
                                self.speak = self.speak + self.user.name
                            elif sentence[1:] == "money":
                                self.speak = self.speak + self.user.balance
                        elif sentence != '+':
                            self.speak = self.speak + sentence.strip('"')
                    print(self.speak)
                    self.speak = ""
                elif item[0] == "Wait":
                    self.waitTime = item[1]
                    timer_thread = threading.Thread(target=self.timer)
                    timer_thread.start()
                elif item[0] == "Branch":
                    if not self.input:
                        self.input = self.input_with_timeout()
                        if self.input is None:
                            print("输入超时，退出程序")
                            self.stop = True
                            return  #
                    # print(item[1].split('"')[1])
                    if item[1].split('"')[1] == self.input:
                        print("收到输入")

    # class Action:


#     """
#
#     """
#     def __init__(self):
#         self.speak = ""
#         self.step = []
#
#     def initialize


def interpreter(action: Action, file_list: list):
    """
    解释脚本语言，根据脚本生成树执行对应的动作

    @param action:
    @param file_list:
    @return:
    """
    global stop_loop
    action.get_script(file_list)
    action.user.login()
    action.fill_stepDic()
    action.initialize_step()
    while True:
        action.execute_script()
        if action.stop:
            break
        time.sleep(0.1)


if __name__ == '__main__':
    files = ['D:/python project/dsl/example.txt']
    act = Action()
    interpreter(act, files)
