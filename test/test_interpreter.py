from interpreter.interpreter import *
import ast
from interpreter.wait import *


def test_get_script():
    action = Action()
    with open("../test/list/parser_list.txt", 'r', encoding='utf-8') as files, open(
            "../test/results/parser_results.txt", 'r', encoding='utf-8') as results:
        for line1, line2 in zip(files, results):
            file = [line1.strip()]
            result = ast.literal_eval(line2)
            action.get_script(file)
            assert action.script == result


def test_initialize_step():
    action = Action()
    with open("../test/list/parser_list.txt", 'r', encoding='utf-8') as files, open(
            "../test/results/step_results.txt", 'r', encoding='utf-8') as results:
        for line1, line2 in zip(files, results):
            file = [line1.strip()]
            result = ast.literal_eval(line2)
            action.get_script(file)
            action.initialize_step()
            assert action.step == result
            assert action.currentStep == result


def test_execute_script(capsys):
    file = ['D:/python project/dsl/example/example2.txt']
    action = Action()
    action.get_script(file)
    action.user.login()

    action.fill_stepDic()
    action.initialize_step()
    # action.input = ""
    action.execute_script()
    captured = capsys.readouterr()
    assert captured.out == 'test1，您好，请问有什么可以帮您?\n这是一条测试语句\n您当前的输入不符合标准，将返回初始界面\n'
