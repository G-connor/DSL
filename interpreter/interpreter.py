# coding: utf-8
# Project: dsl
# File: interpreter.py
# Author: 郭骐畅
# Date: 2023/11/27 21:37

from parsing.parser import *
from user import *
import time
from wait import *


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

    # def timer(self):
    #     """
    #     用于计时
    #
    #     @return:
    #     """
    #     time.sleep(self.waitTime)
    #     self.isTimeout = True

    # def input_with_timeout(self):
    #     """
    #     获取用户输入，如果在超时时间内未输入，则返回 None
    #
    #     @return:
    #     """
    #     input_queue = queue.Queue()
    #
    #     def get_input():
    #         try:
    #             input_queue.put(input())
    #         except:
    #             pass  # 可能需要处理特定的异常
    #
    #     input_thread = threading.Thread(target=get_input)
    #     input_thread.daemon = True
    #     input_thread.start()
    #
    #     while not input_thread.is_alive():
    #         if self.isTimeout:
    #             return None
    #         time.sleep(0.1)  # 稍微等待一下，避免过于频繁的检查
    #
    #     input_thread.join()  # 等待用户输入线程结束
    #     if not self.isTimeout:
    #         return input_queue.get()
    #     else:
    #         return None

    def execute_script(self):
        """
        执行具体脚本

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
                    print(self.speak)
                    self.speak = ""
                elif item[0] == "Wait":
                    self.waitTime = item[1]
                    # timer_thread = threading.Thread(target=self.timer)
                    # timer_thread.start()
                elif item[0] == "Branch":
                    if not self.input:
                        self.input = input_with_timeout(self.waitTime)
                    # print(item[1].split('"')[1])
                    if item[1].split('"')[1] == self.input:
                        self.isSpeakCorrect = True
                        self.stepID = self.stepDic[item[2][0]]
                        self.step = self.script[self.stepID]
                        self.currentStep = list(self.step)
                        self.input = ""
                        return
                elif item[0] == "Default":
                    if self.input != "退出" and self.input != "":
                        print("您当前的输入不符合标准，将返回初始界面")
                        self.step = self.script[0]
                        self.currentStep = list(self.step)
                        self.input = ""
                        return
                elif item == 'Exit':
                    if not self.input:
                        self.input = input_with_timeout(self.waitTime)
                    if self.input == "退出":
                        self.isOver = True
                        return
                    else:
                        print("您当前的输入不符合标准，将返回初始界面")
                        self.step = self.script[0]
                        self.currentStep = list(self.step)
                        self.input = ""
                        return


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
    action.get_script(file_list)
    action.user.login()
    action.fill_stepDic()
    action.initialize_step()
    while True:
        action.execute_script()
        if action.isOver:
            break
        time.sleep(0.1)
    print("您已退出程序，欢迎下次光临")


if __name__ == '__main__':
    files = ['D:/python project/dsl/example.txt']
    act = Action()
    interpreter(act, files)
