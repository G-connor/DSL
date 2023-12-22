import pytest
from parsing.parser import *
import ast


def test_parser():
    with open("../test/list/parser_list.txt", 'r', encoding='utf-8') as files, open(
            "../test/results/parser_results.txt", 'r', encoding='utf-8') as results:
        for line1, line2 in zip(files, results):
            file = [line1.strip()]
            result = ast.literal_eval(line2)
            assert get_files(file) == result
