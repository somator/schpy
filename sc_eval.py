import math
from sc_parser import *
from sc_lexer import *

global_env = {}

def eval_exp(exp, env):
    if exp.type == 'INT':
        return int(exp.data)
    elif exp.type == 'SYMBOL':
        if exp.is_atomic():
            return env[exp.data]
        else: # if symbol is name of a function and not a variable
            local_env = {}
            (variables, definition) = env[exp.data]
            for i in range(len(variables)):
                argument = exp.children[i]
                for child in definition.children:
                    if child.data == variables[i].data:
                        local_env[child.data] = eval_exp(argument, env)
            return eval_exp(definition, local_env)            
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
        if exp.children[0].is_atomic():
            global_env[new_exp_var.data] = eval_exp(new_exp_val, env)
        else:
            global_env[new_exp_var.data] = (new_exp_var.children, new_exp_val)
    elif exp.data == 'if':
        test_exp = exp.children[0]
        then_exp = exp.children[1]
        else_exp = exp.children[2]
        if eval_exp(test_exp, env):
            return eval_exp(then_exp, env)
        else:
            return eval_exp(else_exp, env)
    else:
        raise Exception("Unknown expression type: " + exp.data)

def sc_eval(exp):
    return eval_exp(exp, global_env)