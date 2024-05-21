'''
    正規表現を使ってシェルに渡されたコマンド文字列を解析するモジュール
'''
import re
import enum
import dataclasses
from typing import List

class TokenType(enum.Enum):
    '''
        トークンの種類を表す列挙型
    '''
    STRING = enum.auto()
    PIPE = enum.auto()
    REDIRECT = enum.auto()
    APPEND = enum.auto()
    SEMICOLON = enum.auto()
    AND = enum.auto()
    OR = enum.auto()

@dataclasses.dataclass
class Token:
    '''
        トークンを表すクラス
    '''
    type: TokenType
    value: str

def parse_input(input_str:str) -> List[Token]:
    '''
        シェルに渡されたコマンド文字列を解析する関数
        Args:
            input_str: シェルに渡されたコマンド文字列
        Returns:
            トークンのリスト
    '''
    tokens = []
    for token in re.finditer(r'(?P<STRING>[^\s|&;<>]+)|(?P<PIPE>\|)|(?P<REDIRECT><)|(?P<APPEND>>)|(?P<SEMICOLON>;)|(?P<AND>&&)|(?P<OR>\|\|)', input_str):
        for name, value in token.groupdict().items():
            if value:
                tokens.append(Token(TokenType[name], value))
    return tokens

if __name__ == '__main__':
    command = 'ls -l && echo tetete | grep test > input.txt'
    tokens = parse_input(command)
    for token in tokens:
        print(token)
