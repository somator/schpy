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

    def __str__(self):
        return f'<Node: data={self.data}>'

    def __repr__(self):
        return str(self)

    def add_child(self, child):
        self.children.append(child)