from sc_lexer import *

class Equality:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

class Node(Equality):
    def __init__(self, token):
        self.type = token.tokenType
        self.data = token.data
        self.children = []
        self.parent = None

    def __str__(self):
        return f'<Node: data = \'{self.data}\'>'

    def __repr__(self):
        return str(self)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def is_atomic(self):
        return len(self.children) == 0

def start_parse(inp):
    token_iter = iter(inp)
    try:
        current_token = next(token_iter)
        if current_token.data == '(':
            ast = new_exp(token_iter)
        else:
            ast = Node(current_token)
    except StopIteration:
        raise Exception("Parser received no input.")  
    return ast

def new_exp(token_iter):
    exp = Node(next(token_iter))
    if exp.data == '(':
        exp = Node(Token('', 'COMPOSITE'))
        exp.add_child(new_exp(token_iter))
    while True:
        try:
            current_token = next(token_iter)
            if current_token.data == '(':
                exp.add_child(new_exp(token_iter))
            elif current_token.data == ')':
                break
            else:
                exp.add_child(Node(current_token))
        except StopIteration:
            raise Exception("Incomplete expression.")
    return exp