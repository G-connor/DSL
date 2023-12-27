# coding: utf-8
# Project: dsl
# File: user.py
# Author: 郭骐畅
# Date: 2023/11/27 21:43

class User:
    """
        模拟用户类
    """

    def __init__(self):
        self.name = ""
        self.balance = 0

    def login(self):
        self.name = "test1"
        self.balance = 100
