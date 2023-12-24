import tkinter as tk
from tkinter import simpledialog


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("客服聊天")
        self.text_area = tk.Text(self.root, font=('Arial', 12), bg='#f0f0f0', fg='black', relief=tk.FLAT)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.input_result = None
        self.input_window = None  # 用户输入窗口
        self.is_input_time_out = False

    def gui_print(self, message):
        if self.text_area:
            self.text_area.insert(tk.END, str(message) + "\n")

    def gui_input(self, prompt, time):
        self.is_input_time_out = False
        self.input_result = None

        # 创建用户输入窗口
        self.input_window = tk.Toplevel(self.root)
        self.input_window.title("输入")
        label = tk.Label(self.input_window, text=prompt)
        label.pack()
        self.input_entry = tk.Entry(self.input_window)
        self.input_entry.pack()
        self.input_entry.focus_set()

        # 创建提交按钮
        submit_button = tk.Button(self.input_window, text="输入", command=self._handle_input_submit, bg="blue",
                                  fg="white")
        submit_button.pack(side=tk.BOTTOM, padx=5)

        # 启动定时器，超时后关闭窗口
        self.root.after(time * 1000, self._close_input_window)

        # 等待用户输入
        self.input_window.wait_window(self.input_window)

        if self.is_input_time_out:
            return None
        else:
            return self.input_result

    def _close_input_window(self):
        if self.input_window:
            self.is_input_time_out = True
            self.input_result = None
            self.input_window.destroy()

    def _handle_input_submit(self):
        self.input_result = self.input_entry.get()
        self.gui_print("用户: " + self.input_result)  # 将用户的输入也显示在对话框内
        self.input_window.destroy()

    def start(self):
        self.root.mainloop()


# 创建GUI对象
gui = GUI()


def gui_print(message):
    gui.gui_print(message)


def gui_input(prompt, time=10):
    return gui.gui_input(prompt, time)


if __name__ == "__main__":
    gui.start()
