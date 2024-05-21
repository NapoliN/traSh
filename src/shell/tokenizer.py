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
    REDIRECT_FILE_IN = enum.auto()
    REDIRECT_FILE_OUT = enum.auto()
    REDIRECT_CHANNEL_OUT = enum.auto()
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

def tokenize(input_str:str) -> List[Token]:
    '''
        シェルに渡されたコマンド文字列を解析する関数
        Args:
            input_str: シェルに渡されたコマンド文字列
        Returns:
            トークンのリスト
    '''
    tokens = []
    for token in re.finditer(r'(?P<STRING>[^\s|&;<>]+)|(?P<PIPE>\|)|(?P<REDIRECT_CHANNEL_OUT>>>)|(?P<REDIRECT_FILE_IN><)|(?P<REDIRECT_FILE_OUT>>(?!>))|(?P<SEMICOLON>;)|(?P<AND>&&)|(?P<OR>\|\|)', input_str):
        for name, value in token.groupdict().items():
            if value:
                tokens.append(Token(TokenType[name], value))
    return tokens
