# coding: utf-8
# Project: dsl
# File: wait.py
# Author: 郭骐畅
# Date: 2023/11/28 15:54

import threading
import sys


class InputThread(threading.Thread):
    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
        self.input_text = None

    def run(self):
        try:
            self.input_text = input(self.prompt)
        except EOFError:
            pass  # 输入结束符，例如Ctrl+D


def input_with_timeout(x, y):
    input_prompt = ""

    input_thread = InputThread(input_prompt)
    input_thread.start()
    input_thread.join(x)

    if input_thread.is_alive():
        # 如果线程仍在运行，说明超过了x秒
        print("Timeout reached. Still waiting...")

        # 给输入线程额外的时间，如果超过y秒，就退出程序
        input_thread.join(y - x)

        if input_thread.is_alive():
            print("Timeout reached. Exiting program.")
            sys.exit(1)
        else:
            print("Continuing program...")

    user_input = input_thread.input_text
    # print(f"You entered: {user_input}")
    return user_input


# 示例调用

result = input_with_timeout(2, 4)
print(result)
for i in range(1, 10):
    i = i + 1
    print(i)
