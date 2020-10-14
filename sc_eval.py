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
            (params, body) = env[exp.data]
            for i in range(len(params)):
                param_val = exp.children[i]
                param = params[i].data
                local_env = local_assignment(param_val, body, param, local_env, env)
            # local_env.update(env)
            return eval_exp(body, local_env)
    elif exp.type == 'COMPOSITE':
        return eval_exp(exp.children[0], env)           
    elif exp.data == '*':
        return math.prod([eval_exp(sub_exp, env) for sub_exp in exp.children])
    elif exp.data == '+':
        return sum([eval_exp(sub_exp, env) for sub_exp in exp.children])
    elif exp.data == '-':
        if len(exp.children) >= 2:
            return eval_exp(exp.children[0], env) - sum([eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])
        else:
            return - eval_exp(exp.children[0], env)
    elif exp.data == '/':
        return eval_exp(exp.children[0], env) / math.prod([eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])
    elif exp.data in ['<=', '>=', '<', '>']:
        (op, arg1, arg2) = (exp.data, eval_exp(exp.children[0], env), eval_exp(exp.children[1], env))
        return eval(str(arg1) + op + str(arg2))
    elif exp.data == '=':
        (arg1, arg2) = eval_exp(exp.children[0], env), eval_exp(exp.children[1], env)
        return eval(str(arg1) + '==' + str(arg2))
    elif exp.data == 'define':
        new_exp_var = exp.children[0]
        new_exp_val = exp.children[1]
        if new_exp_var.is_atomic():
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
    elif exp.data == 'lambda':
        params_head = exp.children[0]
        params = [params_head] + params_head.children
        body = exp.children[1]
        local_env = {}
        siblings = exp.parent.children
        args = siblings[siblings.index(exp) + 1:]
        for i in range(len(params)):
            param_val = args[i]
            param = params[i].data
            local_env = local_assignment(param_val, body, param, local_env, env)
        local_env.update(env)
        return eval_exp(body, local_env)
    elif exp.data == 'begin':
        for child in exp.children[:-1]:
            eval_exp(child, env)
        tail_index = len(exp.children) - 1
        return eval_exp(exp.children[tail_index], env)
    elif exp.data == 'cond':
        for child in exp.children:
            if eval_exp(child.children[0], env):
                return eval_exp(child.children[1], env)
    else:
        raise Exception("Unknown expression type: " + exp.data)

def sc_eval(exp):
    return eval_exp(exp, global_env)

def local_assignment(param_val, body, param, local_env, env):
    for child in body.children:
        if child.data == param:
            local_env[child.data] = eval_exp(param_val, env)
        local_env = local_assignment(param_val, child, param, local_env, env)
    return local_env