'''
ASTを生成するモジュール
'''

import dataclasses
from typing import List
from .cmd_parser import TokenType, Token

@dataclasses.dataclass
class Node:
    '''
        ASTのノードを表すクラス
    '''
    type: TokenType

    def __str__(self):
        return f'{self.type}'

    def __repr__(self):
        return self.__str__()

@dataclasses.dataclass
class NodePipe(Node):
    '''
        パイプを表すノード
    '''
    left: Node
    right: Node
    
@dataclasses.dataclass
class NodeRedirect(Node):
    '''
        入力リダイレクトを表すノード
    '''
    cmd: Node
    input: Node
    
@dataclasses.dataclass
class NodeAppend(Node):
    '''
        出力リダイレクトを表すノード
    '''
    cmd: Node
    output: Node

@dataclasses.dataclass
class NodeCommand(Node):
    '''
        コマンドを表すノード
    '''
    cmd: str
    
@dataclasses.dataclass
class NodeConcat(Node):
    '''
        複数のコマンドを表すノード
    '''
    left: Node
    right: Node
    

    
def build_ast(tokens: List[Token]) -> Node:
    '''
        トークンのリストからASTを構築する関数
        Args:
            tokens: トークンのリスト
        Returns:
            ASTのルートノード
        expr = cmd
             = cmd | expr
             = cmd > expr
             = cmd < expr
        cmd = CMDNAME args
        args = ARG
             | ARG args
        args = arg | arg args
    '''
    if not tokens:
        return None
    
    token = tokens.pop(0)
    if token.type == TokenType.STRING:
        return NodeCommand(token.type, token.value)
    if token.type == TokenType.PIPE:
        left = build_ast(tokens)
        right = build_ast(tokens)
        return NodePipe(token.type, left, right)
    if token.type == TokenType.REDIRECT:
        cmd = build_ast(tokens)
        input_ = build_ast(tokens)
        return NodeRedirect(token.type, cmd, input_)
    if token.type == TokenType.APPEND:
        cmd = build_ast(tokens)
        output = build_ast(tokens)
        return NodeAppend(token.type, cmd, output)
    if token.type == TokenType.SEMICOLON:
        left = build_ast(tokens)
        right = build_ast(tokens)
        return NodeConcat(token.type, left, right)

def build_expr(tokens: List[Token]) -> Node:
    node = build_cmd(tokens)
    if not tokens:
        return node
    conj = tokens.pop(0)
    if conj.type == TokenType.PIPE:
        right = build_expr(tokens)
        return NodePipe(conj.type, node, right)

def build_cmd(tokens: List[Token]) -> Node:
    if not tokens:
        return None
    token = tokens.pop(0)
    if token.type == TokenType.STRING:
        return NodeCommand(token.type, token.value)
    if token.type == TokenType.REDIRECT:
        cmd = build_cmd(tokens)
        input_ = build_cmd(tokens)
        return NodeRedirect(token.type, cmd, input_)
    if token.type == TokenType.APPEND:
        cmd = build_cmd(tokens)
        output = build_cmd(tokens)
        return NodeAppend(token.type, cmd, output)

def build_pipe(tokens: List[Token]) -> Node:
    '''
        パイプを表すASTを構築する関数
        Args:
            tokens: トークンのリスト
        Returns:
            パイプを表すASTのルートノード
    '''
    if not tokens:
        return None
    
    token = tokens.pop(0)
    if token.type == TokenType.STRING:
        return NodeCommand(token.type, token.value)
    if token.type == TokenType.PIPE:
        left = build_pipe(tokens)
        right = build_pipe(tokens)
        return NodePipe(token.type, left, right)
    
