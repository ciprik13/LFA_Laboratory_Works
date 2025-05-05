from enum import Enum

class TokenType(Enum):
    NUMBER = 'NUMBER'
    ALL = 'ALL'
    COMPARATOR = 'COMPARATOR'
    COMMA = 'COMMA'
    END = 'END'
    ID = 'ID'
    SELECT = 'SELECT'
    FROM = 'FROM'
    WHERE = 'WHERE'
    ORDER_BY = 'ORDER_BY'
