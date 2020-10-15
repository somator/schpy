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
        if exp.is_atomic():
            if exp.type == 'INT':
                return int(exp.data)
            elif exp.type == 'FLOAT':
                return float(exp.data)
            elif exp.type == 'SYMBOL':
                return env[exp.data]
            else:
                raise Exception('Atomic expression could not be evaluated')
        elif exp.type == 'LIST':
            head = exp.children[0]
            if head.data in self.switch:
                return self.switch[head.data](exp, env)
            elif head.data in env:
                local_env = {}
                (params, body) = env[head.data]
                operands = exp.children[1:]
                for i in range(len(params)):
                    param_val = operands[i]
                    param = params[i].data
                    local_env = self.local_assignment(param_val, body, param, local_env, env)
                # local_env.update(env)
                return self.eval_exp(body, local_env)
            else:
                return self.eval_exp(head, env)
        else:
            raise Exception('Unknown expression type: ' + exp.data)

    def eval_prod(self, exp, env):
        return math.prod([self.eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])

    def eval_sum(self, exp, env):
        return sum([self.eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])

    def eval_minus(self, exp, env):
        if len(exp.children) >= 3:
            return self.eval_exp(exp.children[1], env) - sum([self.eval_exp(sub_exp, env) for sub_exp in exp.children[2:]])
        else:
            return - self.eval_exp(exp.children[1], env)

    def eval_div(self, exp, env):
        return self.eval_exp(exp.children[1], env) / math.prod([self.eval_exp(sub_exp, env) for sub_exp in exp.children[2:]])

    def eval_comparison(self, exp, env):
        (op, arg1, arg2) = (exp.children[0].data, self.eval_exp(exp.children[1], env), self.eval_exp(exp.children[2], env))
        return eval(str(arg1) + op + str(arg2))

    def eval_eq(self, exp, env):
        (arg1, arg2) = self.eval_exp(exp.children[1], env), self.eval_exp(exp.children[2], env)
        return arg1 == arg2

    def eval_def(self, exp, env):
        name_and_params = exp.children[1]
        body = exp.children[2]
        if name_and_params.is_atomic():
            self.global_env[name_and_params.data] = self.eval_exp(body, env)
        else:
            self.global_env[name_and_params.children[0].data] = (name_and_params.children[1:], body)

    def eval_if(self, exp, env):
        test_exp = exp.children[1]
        then_exp = exp.children[2]
        else_exp = exp.children[3]
        if self.eval_exp(test_exp, env):
            return self.eval_exp(then_exp, env)
        else:
            return self.eval_exp(else_exp, env)

    def eval_lambda(self, exp, env):
        params = exp.children[1].children
        body = exp.children[2]
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
        for child in exp.children[1:-1]:
            self.eval_exp(child, env)
        tail_index = len(exp.children) - 1
        return self.eval_exp(exp.children[tail_index], env)

    def eval_cond(self, exp, env):
        for child in exp.children[1:]:
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