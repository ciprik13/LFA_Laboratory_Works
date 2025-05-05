from token_type import TokenType
from ast_node import ASTNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else None

    def advance(self):
        self.current += 1

    def match(self, *token_types):
        if self.peek() and self.peek().kind in token_types:
            tok = self.peek()
            self.advance()
            return tok
        return None

    def expect(self, *token_types):
        tok = self.match(*token_types)
        if not tok:
            expected = ', '.join(t.name for t in token_types)
            actual = self.peek().kind.name if self.peek() else "EOF"
            raise RuntimeError(f"Expected {expected}, but got {actual}")
        return tok

    def parse(self):
        nodes = []
        while self.peek():
            if self.peek().kind == TokenType.SELECT:
                nodes.append(self.select_statement())
            else:
                self.advance()
        return nodes

    def select_statement(self):
        node = ASTNode('SELECT_STATEMENT')
        self.expect(TokenType.SELECT)
        node.add_child(ASTNode('SELECT'))

        column_list = ASTNode('COLUMN_LIST')
        while True:
            token = self.match(TokenType.ID)
            if not token:
                break
            column_list.add_child(ASTNode('COLUMN', token.value))
            if not self.match(TokenType.COMMA):
                break
        node.add_child(column_list)

        self.expect(TokenType.FROM)
        from_id = self.expect(TokenType.ID)
        node.add_child(ASTNode('FROM', from_id.value))

        if self.match(TokenType.WHERE):
            where = ASTNode('WHERE')
            left_token = self.expect(TokenType.ID, TokenType.NUMBER)
            comp = self.expect(TokenType.COMPARATOR)
            right_token = self.expect(TokenType.ID, TokenType.NUMBER)
            where.add_child(ASTNode('LEFT', left_token.value))
            where.add_child(ASTNode('OP', comp.value))
            where.add_child(ASTNode('RIGHT', right_token.value))
            node.add_child(where)

        if self.match(TokenType.ORDER_BY):
            order_by = self.expect(TokenType.ID)
            node.add_child(ASTNode('ORDER_BY', order_by.value))

        self.match(TokenType.END)
        return node
