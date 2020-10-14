import math
from sc_parser import *
from sc_lexer import *

class Evaluator:
    def __init__(self):
        self.global_env = {}
        self.switch = {
            '*' : self.eval_prod,
            '+' : self.eval_sum,
            '-' : self.eval_minus,
            '/' : self.eval_div,
            '<=' : self.eval_comparison,
            '>=' : self.eval_comparison,
            '<' : self.eval_comparison,
            '>' : self.eval_comparison,
            '=' : self.eval_eq,
            'define' : self.eval_def,
            'if' : self.eval_if,
            'lambda' : self.eval_lambda,
            'begin' : self.eval_begin,
            'cond' : self.eval_cond,
        }

    def eval_exp(self, exp, env):
        if exp.type == 'INT':
            return int(exp.data)
        elif exp.type == 'FLOAT':
            return float(exp.data)
        elif exp.type == 'SYMBOL':
            if exp.is_atomic():
                return env[exp.data]
            else: # if symbol is name of a function and not a variable
                local_env = {}
                (params, body) = env[exp.data]
                for i in range(len(params)):
                    param_val = exp.children[i]
                    param = params[i].data
                    local_env = self.local_assignment(param_val, body, param, local_env, env)
                # local_env.update(env)
                return self.eval_exp(body, local_env)
        elif exp.type == 'COMPOSITE':
            return self.eval_exp(exp.children[0], env)
        elif exp.data in self.switch:
            return self.switch[exp.data](exp, env)
        else:
            raise Exception("Unknown expression type: " + exp.data)

    def eval_prod(self, exp, env):
        return math.prod([self.eval_exp(sub_exp, env) for sub_exp in exp.children])

    def eval_sum(self, exp, env):
        return sum([self.eval_exp(sub_exp, env) for sub_exp in exp.children])

    def eval_minus(self, exp, env):
        if len(exp.children) >= 2:
            return self.eval_exp(exp.children[0], env) - sum([self.eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])
        else:
            return - self.eval_exp(exp.children[0], env)

    def eval_div(self, exp, env):
        return self.eval_exp(exp.children[0], env) / math.prod([self.eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])

    def eval_comparison(self, exp, env):
        (op, arg1, arg2) = (exp.data, self.eval_exp(exp.children[0], env), self.eval_exp(exp.children[1], env))
        return eval(str(arg1) + op + str(arg2))

    def eval_eq(self, exp, env):
        (arg1, arg2) = self.eval_exp(exp.children[0], env), self.eval_exp(exp.children[1], env)
        return arg1 == arg2

    def eval_def(self, exp, env):
        new_exp_var = exp.children[0]
        new_exp_val = exp.children[1]
        if new_exp_var.is_atomic():
            self.global_env[new_exp_var.data] = self.eval_exp(new_exp_val, env)
        else:
            self.global_env[new_exp_var.data] = (new_exp_var.children, new_exp_val)

    def eval_if(self, exp, env):
        test_exp = exp.children[0]
        then_exp = exp.children[1]
        else_exp = exp.children[2]
        if self.eval_exp(test_exp, env):
            return self.eval_exp(then_exp, env)
        else:
            return self.eval_exp(else_exp, env)

    def eval_lambda(self, exp, env):
        params_head = exp.children[0]
        params = [params_head] + params_head.children
        body = exp.children[1]
        local_env = {}
        siblings = exp.parent.children
        args = siblings[siblings.index(exp) + 1:]
        for i in range(len(params)):
            param_val = args[i]
            param = params[i].data
            local_env = self.local_assignment(param_val, body, param, local_env, env)
        local_env.update(env)
        return self.eval_exp(body, local_env)

    def eval_begin(self, exp, env):
        for child in exp.children[:-1]:
            self.eval_exp(child, env)
        tail_index = len(exp.children) - 1
        return self.eval_exp(exp.children[tail_index], env)

    def eval_cond(self, exp, env):
        for child in exp.children:
            if self.eval_exp(child.children[0], env):
                return self.eval_exp(child.children[1], env)

    def local_assignment(self, param_val, body, param, local_env, env):
        for child in body.children:
            if child.data == param:
                local_env[child.data] = self.eval_exp(param_val, env)
            local_env = self.local_assignment(param_val, child, param, local_env, env)
        return local_env

    def sc_eval(self, exp):
        return self.eval_exp(exp, self.global_env)

    def lex_parse_eval(self, input):
        lexed = sc_lex(input)
        ast = start_parse(lexed)
        return self.sc_eval(ast)