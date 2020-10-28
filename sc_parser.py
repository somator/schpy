from sc_lexer import *

class Equality:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

# The AST (abstract syntax tree) is comprised of nodes containing 2 strings, representing type
# and data, a list of children nodes, and an optional parent node (used for lambda evaluation).
# Nodes can be either atomic, meaning they contain no children/arguments (i.e. numbers or variables), 
# or list nodes, which require more in-depth evaluation.
class Node(Equality):
    def __init__(self, **kwargs):
        self.type = ''
        self.data = ''
        self.parent = None
        self.__dict__.update(kwargs)
        self.children = []

    def __str__(self):
        if self.type != 'LIST':
            return f'<Node: data = \'{self.data}\'>'
        else:
            return str(self.children)

    def __repr__(self):
        return str(self)

    def add_child(self, child):
        self.children.append(child)

    def is_atomic(self):
        return len(self.children) == 0

    def next_sibling(self):
        siblings = self.parent.children
        return siblings[siblings.index(self) + 1]

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

# Takes a tokenized input and returns an AST. If the first token is not a left parenthesis, the
# AST should be an atom, and otherwise, a list.
def start_parse(inp):
    token_iter = iter(inp)
    try:
        current_token = next(token_iter)
        if current_token.data == '(':
            ast = new_exp(token_iter)
        else:
            ast = Node(type=current_token.tokenType, data=current_token.data)
    except StopIteration:
        raise Exception("Parser received no input.")  
    return ast

# Generates a list node and assigns it children according to each token in the iterator, recurring
# whenever the next token is a left parenthesis, and finally returning the list node when the next
# token is a right parenthesis.
def new_exp(token_iter):
    exp = Node(type='LIST')
    head = next(token_iter)
    if head.data == '(':
        exp.add_child(new_exp(token_iter))
    else:
        exp.add_child(Node(type=head.tokenType, data=head.data, parent=exp))
    while True:
        try:
            current_token = next(token_iter)
            if current_token.data == '(':
                exp.add_child(new_exp(token_iter))
            elif current_token.data == ')':
                break
            else:
                exp.add_child(Node(type=current_token.tokenType, data=current_token.data, parent=exp))
        except StopIteration:
            raise Exception("Incomplete expression.")
    return exp