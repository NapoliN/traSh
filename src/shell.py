'''
シェルを提供するモジュール
'''
import cmd
import sys
import io
from typing import List, Optional
from .cmd_parser import parse_input, TokenType

class ShellEmulator(cmd.Cmd):
    '''
        パイプとかリダイレクトとかを考慮したシェルエミュレータ
    '''
    def __init__(self) -> None:
        super().__init__()
        self.prompt = '>>> '
        self.conjqueue: List[TokenType] = []
        self.accept = True
        self.stream : Optional[io.StringIO] = None
        self.fstream : Optional[io.TextIOWrapper] = None

    def precmd(self, line: str) -> str:
        '''
            コマンド文字列を解析してトークンのリストを作成する    
        '''
        if self.accept:
            # 受理可能状態の場合は、入力をparseする
            tokens = parse_input(line)
            while tokens:
                cmd = ""
                while tokens and tokens[0].type == TokenType.STRING:
                    token = tokens.pop(0)
                    cmd += token.value + " "
                self.cmdqueue.append(cmd)

                if tokens:
                    conj = tokens.pop(0)
                    self.conjqueue.append(conj.type)
            self.accept = False
            line = self.cmdqueue.pop(0)

        if self.stream:
            # pipeされた入力を受け取る
            sys.stdout = sys.__stdout__
            line += self.stream.getvalue()
            self.stream.close()
            self.stream = None
        
        if self.fstream:
            # リダイレクトされた入力を受け取る
            sys.stdin = sys.__stdin__
            line += self.fstream.read()
            self.fstream.close()
            self.fstream = None

        if self.conjqueue:
            conjtype = self.conjqueue.pop(0)
            if conjtype == TokenType.PIPE:
                self.stream = io.StringIO()
                sys.stdout = self.stream
            if conjtype == TokenType.APPEND:
                fname = self.cmdqueue.pop(0)
                p = open(fname, 'a', encoding='utf-8')
                self.fstream = open(fname, 'w', encoding='utf-8')
                sys.stdout = self.fstream
            if conjtype == TokenType.REDIRECT:
                fname = self.cmdqueue.pop(0)
                self.fstream = open(fname, 'r', encoding='utf-8')
                sys.stdin = self.fstream

        return line
    
    def postcmd(self, stop: bool, line: str) -> bool:
        if not self.cmdqueue:
            # キューを処理しきったので、次のコマンドを受け付ける
            self.accept = True
            if self.stream:
                # リダイレクトされた出力を閉じる
                self.stream.close()
                self.stream = None
                sys.stdout = sys.__stdout__
                
        return super().postcmd(stop, line)

    def do_ping(self,_):
        print("pong")
        
    def do_echo(self, arg):
        print(arg, "ee")

if __name__ == '__main__':
    ShellEmulator().cmdloop()    