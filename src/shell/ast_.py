'''
ASTを生成するモジュール
生成規則
    expr = cmd
         | cmd | expr
         | cmd ; expr
         | cmd && expr
    cmd = CMDNAME args redirects
    args = ARG
        | ARG args
    redirects = > FNAME redirects
              | < FNAME redirects
              | >> CHANNEL_NAME redirects
              | << CHANNEL_NAME redirects
              | ε
'''

import enum
import dataclasses
from typing import List, Optional
from .tokenizer import TokenType, Token

class SyntaxError(Exception):
    '''
        構文エラーを表す例外
    '''
    pass

@dataclasses.dataclass
class Node:
    '''
        ASTのノードを表すクラス
    '''
    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return self.__str__()
    
    def print(self):
        '''
            ASTを出力する
        '''
        print(self.tree())
    
    def tree(self, indent=0) -> str:
        '''
            ASTを出力する
        '''
        return '    '*indent

@dataclasses.dataclass
class NodePipe(Node):
    '''
        パイプを表すノード
    '''
    left: Node
    right: Node
    def tree(self, indent=0):
        return super().tree(indent) + f'|\n{self.left.tree(indent+1)}\n{self.right.tree(indent+1)}'
    
@dataclasses.dataclass
class NodeConcat(Node):
    '''
        複数のコマンドを表すノード
    '''
    left: Node
    right: Node
    
@dataclasses.dataclass
class NodeAnd(Node):
    '''
        論理積を表すノード
    '''
    left: Node
    right: Node

@dataclasses.dataclass
class NodeOr(Node):
    '''
        論理和を表すノード
    '''
    left: Node
    right: Node
    
@dataclasses.dataclass
class NodeRedirect(Node):
    '''
        リダイレクトを表すノード
    '''
    class Type(enum.Enum):
        In = enum.auto()
        Out = enum.auto()
        CHANNEL_OUT = enum.auto()
    type_: Type
    fname: str

@dataclasses.dataclass
class NodeCommand(Node):
    '''
        コマンドを表すノード
    '''
    cmd: str
    args : List[str]
    redirects : Optional[List[NodeRedirect]] = None
    
    def __str__(self):
        return super().__str__() + f'({self.cmd}, {self.args}, {self.redirects})'
    
    def tree(self, indent=0):
        return super().tree(indent) + f'{self.cmd} {self.args} {self.redirects}'

    
class ASTBuilder:
    '''
        ASTを構築するクラス
    '''
    def __init__(self) -> None:
        self.index = 0
        self.tokens: List[Token] = []

    @property
    def current_token(self) -> Token:
        '''
            現在のトークンを返す
        '''
        return self.tokens[self.index]
    
    @property
    def is_end(self) -> bool:
        '''
            トークン列の終端に達しているかどうか
        '''
        return self.index >= len(self.tokens)
    
    def pop_token(self) -> Token:
        '''
            トークンを一つ進める
        '''
        self.index += 1
        return self.tokens[self.index - 1]
    
    def build_ast(self, tokens:List[Token]) -> Node:
        '''
            ASTを構築する
        '''
        self.index = 0
        self.tokens = tokens
        expr = self.build_expr()
        self.index = 0
        self.tokens = []    
        return expr

    def build_expr(self) -> Node:
        '''
            exprを構築する
        '''
        if self.is_end:
            raise SyntaxError('tokens is empty')
        cmd = self.build_cmd()
        if self.is_end:
            return cmd
        token = self.pop_token()
        if token.type == TokenType.PIPE:
            right = self.build_expr()
            return NodePipe(left=cmd, right=right)
        elif token.type == TokenType.SEMICOLON:
            right = self.build_expr()
            return NodeConcat(left=cmd, right=right)
        elif token.type == TokenType.AND:
            right = self.build_expr()
            return NodeAnd(left=cmd, right=right)
        elif token.type == TokenType.OR:
            right = self.build_expr()
            return NodeOr(left=cmd, right=right)
        else:
            raise SyntaxError(f'invalid token {token}')

    def build_cmd(self) -> Node:
        '''
            cmdを構築する
        '''
        if self.is_end:
            raise SyntaxError('tokens is empty')
        
        token = self.pop_token()
        if token.type != TokenType.STRING:
            raise SyntaxError('CMDNAME is not found')
        cmdname = token.value
        
        args = []
        while not self.is_end and self.current_token.type == TokenType.STRING:
            token = self.pop_token()
            args.append(token.value)
        
        cmd = NodeCommand(cmd=cmdname, args=args)
        
        if not self.is_end and (self.current_token.type == TokenType.REDIRECT_FILE_IN or self.current_token.type == TokenType.REDIRECT_FILE_OUT or self.current_token.type == TokenType.REDIRECT_CHANNEL_OUT):
            redirects = self.build_redirects()
            cmd.redirects = redirects
        return cmd

    def build_redirects(self) -> List[NodeRedirect]:
        '''
            redirectsを構築する
        '''
        redirects: List[NodeRedirect] = []
        while not self.is_end and (self.current_token.type == TokenType.REDIRECT_FILE_IN or self.current_token.type == TokenType.REDIRECT_FILE_OUT or self.current_token.type == TokenType.REDIRECT_CHANNEL_OUT):
            token = self.pop_token()
            if token.type == TokenType.REDIRECT_FILE_OUT:
                type_ = NodeRedirect.Type.Out
            elif token.type == TokenType.REDIRECT_FILE_IN:
                type_ = NodeRedirect.Type.In
            elif token.type == TokenType.REDIRECT_CHANNEL_OUT:
                type_ = NodeRedirect.Type.Out
            else:
                raise SyntaxError(f'invalid token {token}')
            if self.is_end or self.current_token.type != TokenType.STRING:
                raise SyntaxError('FNAME is not found')
            fname = self.pop_token().value
            redirects.append(NodeRedirect(type_=type_, fname=fname))
        return redirects