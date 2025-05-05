from lexer import Lexer
from parser import Parser

code_test = '''
    SELECT col1, col2, col3 FROM table1 WHERE col1 >= 30 ORDER_BY col2;
    SELECT col4 FROM table2 WHERE 1==1;
'''

lexer = Lexer(code_test)
tokens = lexer.tokenize()

parser = Parser(tokens)
asts = parser.parse()

for ast in asts:
    print(ast)
