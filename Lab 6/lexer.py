import re
from token_type import TokenType


class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.kind}, {repr(self.value)}, line={self.line}, column={self.column})"

    def print_token(self):
        print(f"Token(type={self.kind}, value='{self.value}', line={self.line}, column={self.column})")


class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        code = self.code
        keywords = {"SELECT", "FROM", "WHERE", "ORDER_BY"}
        token_specification = [
            ('NUMBER', r'\d+(\.\d*)?'),
            ('ALL', r'\*'),
            ('COMPARATOR', r'(==|>=|<=|<>|>|<)'),
            ('COMMA', r','),
            ('END', r';'),
            ('ID', r'[a-zA-Z][a-zA-Z_$0-9]*'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join(f'(?P<{kind}>{pattern})' for kind, pattern in token_specification)
        line_num = 1
        line_start = 0
        tokens = []

        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start

            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
                kind_enum = TokenType.NUMBER
            elif kind == 'ID':
                if value in keywords:
                    kind_enum = TokenType[value]
                else:
                    kind_enum = TokenType.ID
            elif kind == 'ALL':
                kind_enum = TokenType.ALL
            elif kind == 'COMPARATOR':
                kind_enum = TokenType.COMPARATOR
            elif kind == 'COMMA':
                kind_enum = TokenType.COMMA
            elif kind == 'END':
                kind_enum = TokenType.END
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            else:
                raise RuntimeError(f"Unhandled token type: {kind}")

            token = Token(kind_enum, value, line_num, column)
            tokens.append(token)
            token.print_token()

        return tokens
