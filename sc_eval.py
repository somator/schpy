import math
from sc_parser import *

def eval_exp(exp):
    if exp.type == 'INT':
        return int(exp.data)
    elif exp.data == '*':
        return math.prod([eval_exp(sub_exp) for sub_exp in exp.children])
    elif exp.data == '+':
        return sum([eval_exp(sub_exp) for sub_exp in exp.children])
    elif exp.data == '-':
        return eval_exp(exp.children[0]) - sum([eval_exp(sub_exp) for sub_exp in exp.children[1:]])
    elif exp.data == '/':
        return eval_exp(exp.children[0]) / math.prod([eval_exp(sub_exp) for sub_exp in exp.children[1:]])