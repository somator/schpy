import math
from sc_parser import *
from sc_lexer import *

class Evaluator:
    def __init__(self):
        # The global environment is used for any functions or variables that we define with global scope.
        self.global_env = {}
        # switch stores the reserved operators and is used to evaluate non-atomic expressions.
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

    # The primary evaluation method
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
            # head is the first item in the list node, an operator in the case of list expressions.
            head = exp.children[0]
            if head.data in self.switch:
                return self.switch[head.data](exp, env)
            elif head.data in env:
                # the local environment is used to assign parameter values to expression parameters.
                local_env = {}
                (params, body) = env[head.data]
                operands = exp.children[1:]
                for i in range(len(params)):
                    param_val = operands[i]
                    param = params[i].data
                    local_env[param] = self.eval_exp(param_val, env)
                # local_env.update(env)
                return self.eval_exp(body, local_env)
            else:
                return self.eval_exp(head, env)
        else:
            raise Exception('Unknown expression type: ' + exp.data)

    # return the product of the operands of a list expression.
    def eval_prod(self, exp, env):
        return math.prod([self.eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])

    # return the sum of the operands of a list expression.
    def eval_sum(self, exp, env):
        return sum([self.eval_exp(sub_exp, env) for sub_exp in exp.children[1:]])

    # if there are 2 or more operands, return the first minus the rest
    # otherwise return the negative operand.
    def eval_minus(self, exp, env):
        if len(exp.children) >= 3:
            return self.eval_exp(exp.children[1], env) - sum([self.eval_exp(sub_exp, env) for sub_exp in exp.children[2:]])
        else:
            return - self.eval_exp(exp.children[1], env)

    # return the first operand divided by the product of the rest of the operands.
    def eval_div(self, exp, env):
        return self.eval_exp(exp.children[1], env) / math.prod([self.eval_exp(sub_exp, env) for sub_exp in exp.children[2:]])

    # evaluate the comparison between 2 operands according to their comparison operator.
    def eval_comparison(self, exp, env):
        (op, arg1, arg2) = (exp.children[0].data, self.eval_exp(exp.children[1], env), self.eval_exp(exp.children[2], env))
        return eval(str(arg1) + op + str(arg2))

    # return true if the evaluation of 2 operands are equal.
    def eval_eq(self, exp, env):
        (arg1, arg2) = self.eval_exp(exp.children[1], env), self.eval_exp(exp.children[2], env)
        return arg1 == arg2

    # if the first operand is atomic, we store the evaluation of the second operand
    # in the environment at the name of the variable we are defining.
    # otherwise, we are defining an expression, and we store a tuple containing the 
    # names of the parameters and the body of the expression in the environment at
    # the name of expression we are defining.
    def eval_def(self, exp, env):
        name_and_params = exp.children[1]
        body = exp.children[2]
        if name_and_params.is_atomic():
            env[name_and_params.data] = self.eval_exp(body, env)
        else:
            env[name_and_params.children[0].data] = (name_and_params.children[1:], body)

    # evaluate the first operand/test case. if true, return the evaluation of the 
    # first operand, otherwise the evaluation of the second.
    def eval_if(self, exp, env):
        test_exp = exp.children[1]
        then_exp = exp.children[2]
        else_exp = exp.children[3]
        if self.eval_exp(test_exp, env):
            return self.eval_exp(then_exp, env)
        else:
            return self.eval_exp(else_exp, env)

    # identify the parameters and body of the lambda expression, and then evaluate 
    # by retrieving the parameter values from the next sibling of the list node,
    # assigning them to their parameters in a local environment, and evaluating the
    # body of the lambda expression according to the assigned parameters.
    def eval_lambda(self, exp, env):
        params = exp.children[1].children
        body = exp.children[2]
        local_env = {}
        siblings = exp.parent.children
        args = siblings[siblings.index(exp) + 1:]
        for i in range(len(params)):
            param_val = args[i]
            param = params[i].data
            local_env[param] = self.eval_exp(param_val, env)
        local_env.update(env)
        return self.eval_exp(body, local_env)

    # sequentially evaluate each expression in the list and return the last one.
    def eval_begin(self, exp, env):
        for child in exp.children[1:-1]:
            self.eval_exp(child, env)
        tail_index = len(exp.children) - 1
        return self.eval_exp(exp.children[tail_index], env)

    # evaluate the first item of each operand pair sequentially. If true, return the
    # evaluation of the second item.
    def eval_cond(self, exp, env):
        for child in exp.children[1:]:
            if self.eval_exp(child.children[0], env):
                return self.eval_exp(child.children[1], env)

    # evaluate an expression using the global environment.
    def sc_eval(self, exp):
        return self.eval_exp(exp, self.global_env)

    # lex, parse, and evaluate a string.
    def lex_parse_eval(self, input):
        lexed = sc_lex(input)
        ast = start_parse(lexed)
        return self.sc_eval(ast)