import sys

from sc_lexer import *
from sc_parser import *
from sc_eval import Evaluator

class Interpreter:
    def __init__(self):
        self.evaluator = Evaluator()

    def lex_parse_eval(self, inp):
        lexed = sc_lex(inp)
        parsed = start_parse(lexed)
        result = self.evaluator.sc_eval(parsed)
        return result

    def repl(self):
        text = ''
        line = '> '
        paren_balance = 0
        while True:
            inp = input(line)
            if inp == 'exit':
                break
            text = text + ' ' + inp
            line = '> '
            for char in inp:
                if char == '(':
                    paren_balance += 1
                elif char == ')':
                    paren_balance -= 1
            if paren_balance == 0 and inp != '':
                result = self.lex_parse_eval(text)
                if result is not None:
                    print(result)
                text = ''
            elif paren_balance < 0:
                raise Exception('Expression unbalanced. Too many right parentheses.')
            else:
                for i in range(paren_balance):
                    line = line + '\t'

    def interpret_file(self, filename):
        file = open(filename)
        lines = file.readlines()
        file.close()
        paren_balance = 0
        inp = ''
        for line in lines:
            for char in line:
                if char == '(':
                    paren_balance += 1
                elif char == ')':
                    paren_balance -= 1
            inp = inp + line
            if paren_balance == 0 and inp != '':
                result = self.lex_parse_eval(inp)
                if result is not None:
                    print(result)
                inp = ''
                paren_balance == 0
            elif paren_balance < 0:
                raise Exception('Expression unbalanced. Too many right parentheses.')

if __name__ == '__main__':
    interpreter = Interpreter()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        interpreter.interpret_file(filename)
    else:
        interpreter.repl()