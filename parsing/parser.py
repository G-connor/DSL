import pyparsing as pp


class Parser:
    """

    """
    _integer = pp.Regex("[-+]?[0-9]+").set_parse_action(lambda tokens: int(tokens[0]))
    _real = pp.Regex("[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?").set_parse_action(
        lambda tokens: float(tokens[0]))
    _string_constant = pp.quoted_string('"')

    _name = pp.Combine('$' + pp.Regex("[0-9A-Za-z_]+"))
    _plus = pp.Literal('+')
    _minus_with_integer = pp.Literal('-') + _integer
    _exit_action = pp.Keyword("Exit")
    # _goto_action = pp.Group(pp.Keyword("Goto") + pp.Word(pp.alphas))
    _goto_action = pp.Word(pp.alphas)
    _wait = pp.Group(pp.Keyword("Wait") + _integer)
    _branch = pp.Group(pp.Keyword("Branch") + _string_constant + pp.Group(_goto_action))
    _default = pp.Group(pp.Keyword("Default") + pp.Group(_goto_action))
    _speak_content = _name ^ _string_constant
    _speak_content_action = pp.Group(pp.Keyword("Speak") + pp.Group(
        _speak_content + pp.ZeroOrMore('+' + _speak_content)).set_parse_action(lambda tokens: tokens[0::2]))
    _change = pp.Group(pp.Keyword("Change") + _name + pp.Optional(_plus) + pp.Optional(_minus_with_integer))

    _step = pp.Group(pp.Keyword("Step") + pp.Word(pp.alphas) + pp.Group(
        pp.ZeroOrMore(_speak_content_action)) + pp.Group(_wait) + pp.Group(pp.ZeroOrMore(_change))+pp.Group(
        pp.ZeroOrMore(_speak_content_action))
                     + pp.Group(pp.ZeroOrMore(_branch)) + pp.Group(pp.ZeroOrMore(_default))
                     + pp.Group(_exit_action))

    language = pp.ZeroOrMore(_step)


def get_files(files: list):
    """

    @param files:
    @return:
    """
    result = []
    for file in files:
        if len(file) == 0:
            continue
        result += Parser.language.parse_file(file, parse_all=True).as_list()
    return result


# class Step:
#     """
#
#     """
#
#     def __init__(self):
#         self.stepId = 0  # 表示当前在哪个阶段
#         self.name = ""  # 当前用户名称
#         self.money = 0  # 当前余额
#         self.speak = ""  # 当前要说的话
#         self.token = ""  # 当前的关键词
#
#
# def process_token(step: Step):
#     if step.token == "Step":
#         process_step(step)
#
#
# def process_step(step:Step):


# class Process:


#     """
#
#     """
#
#     def __init__(self):
#         self.script = []
#         self.stepId = 0
#
#     def get_script(self, l: list):
#         self.script = get_files(l)
#
#     def process_step(self):


if __name__ == '__main__':
    print(get_files(['D:/python project/dsl/example.txt']))
    # p = Process()
    # p.get_script(['D:/python project/dsl/example.txt'])
