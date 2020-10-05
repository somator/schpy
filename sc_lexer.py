import sys
import re

RESERVED = 'RESERVED'
INT = 'INT'

token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'[0-9]+',                INT),
]

class Token:
    def __init__(self, data, tokenType):
        self.data = data
        self.tokenType = tokenType

    def __str__(self):
        return f'<{self.tokenType} Token: {self.data}>'
    
    def __repr__(self):
        return str(self)


def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tokenType = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tokenType:
                    token = Token(text, tokenType)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens

def sc_lex(characters):
    return lex(characters, token_exprs)