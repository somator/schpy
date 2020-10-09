import math
from sc_parser import *

global_env = {}

def eval_exp(exp, env):
    if exp.type == 'INT':
        return int(exp.data)
    elif exp.type == 'SYMBOL':
        if len(exp.children) == 0:
            return env[exp.data]
        else: # if symbol is name of a function and not a variable
            pass
    elif exp.data == '*':
        return math.prod([eval_exp(sub_exp, env) for sub_exp in exp.children])
    elif exp.data == '+':
        return sum([eval_exp(sub_exp, env) for sub_exp in exp.children])
    elif exp.data == '-':
        return eval_exp(exp.children[0], env) - sum([eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])
    elif exp.data == '/':
        return eval_exp(exp.children[0], env) / math.prod([eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])
    elif exp.data == 'define':
        new_exp_var = exp.children[0]
        new_exp_val = exp.children[1]
        if len(exp.children[0].children) == 0:
            global_env[new_exp_var.data] = eval_exp(new_exp_val, env)
        else:
            pass
    else:
        raise Exception("Unknown expression type: " + exp.data)

def sc_eval(exp):
    return eval_exp(exp, global_env)