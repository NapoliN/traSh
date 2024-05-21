'''
シェルを提供するモジュール
'''
import sys
import io
import os
import enum
import dataclasses
from typing import List, Optional, Generator, Tuple
from .tokenizer import tokenize
from .ast_ import ASTBuilder, Node, NodeCommand, NodePipe, NodeRedirect, NodeConcat

import subprocess
                
@dataclasses.dataclass
class ChanneiIO():
    '''
        チャネルを表すクラス
    '''
    class Type(enum.Enum):
        In = enum.auto()
        Out = enum.auto()
    channel_name: str
    type_: Type
                
class ShellBase():
    '''
        シェルを提供するクラス
    '''
    outbuffer: Optional[io.StringIO] = None
    channelIOs: List[ChanneiIO] = []
    def __init__(self):
        self.readable = False
        self.prompt = '>>> '
    
    def run(self):
        while True:
            self.preinput()
            cmd = input(self.prompt)
            if cmd == '':
                continue
            if cmd == 'exit':
                break
            tokens = tokenize(cmd)
            ast = ASTBuilder().build_ast(tokens)
            self.__interpret(ast)
        pass
    
    def preinput(self):
        '''
            入力前のhook関数
        '''
        pass
    
    def precmd(self):
        '''
            コマンド実行前のhook関数
        '''
        pass
    
    def postcmd(self):
        '''
            コマンド実行後のhook関数
        '''
        pass
    
    def do_cd(self, args:List[str]):
        '''
            cdコマンド
            これだけは親プロセスからやる必要がある
            子クラスで実装する
        '''
        pass
    
    def __interpret(self, ast:Node):
        '''
            ASTに従ってコマンドを実行する
        '''
        generator = self.__interpret_internal(ast)
        for cmd, args in generator:
            self.precmd()
            input_: Optional[str] = None
            if self.readable:
                input_ = sys.stdin.read()
                self.readable = False
            script_path = search_script(cmd)
            if cmd == "cd":
                self.do_cd(args)
                self.postcmd()
                continue
            if script_path is not None:
                # src/scripts下にスクリプトがあるならそれを実行
                module_name = path2module(script_path)
                child = subprocess.run(['poetry', 'run', 'python', '-m', module_name, *args],encoding='utf-8',input=input_,stdout=subprocess.PIPE)           
            else:
                # なければ通常のコマンドを実行
                child = subprocess.run([cmd, *args],encoding='utf-8',input=input_,stdout=subprocess.PIPE)
            sys.stdout.write(child.stdout)
            self.postcmd()

    def __interpret_internal(self, ast:Node) -> Generator[Tuple[str, List[str]], None, None]:
        '''
            interpretの内部実装
            NodeCommand訪問時にyieldでコマンドを返す
        '''
        # コマンド処理
        if type(ast) == NodeCommand:
            # リダイレクト処理
            old_stdin = sys.stdin
            old_stdout = sys.stdout
            if ast.redirects:
                for redir in ast.redirects:
                    if redir.type_ == NodeRedirect.Type.In:
                        sys.stdin = open(redir.fname, 'r', encoding='utf-8')
                        self.readable = True
                    if redir.type_ == NodeRedirect.Type.Out:
                        sys.stdout = open(redir.fname, 'w', encoding='utf-8')
                    if redir.type_ == NodeRedirect.Type.CHANNEL_OUT:
                        self.outbuffer = io.StringIO()
                        sys.stdout = self.outbuffer
                        self.channelIOs.append(ChanneiIO(redir.fname, ChanneiIO.Type.Out))
            yield ast.cmd, ast.args
            # リダイレクト復帰処理
            if sys.stdout != old_stdout:
                sys.stdout.close()
                sys.stdout = old_stdout
            if sys.stdin != old_stdin:
                sys.stdin.close()
                sys.stdin = old_stdin
            
        # パイプ処理
        if type(ast) == NodePipe:
            # 標準出力をIOにつなぐ
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            left = self.__interpret_internal(ast.left)
            for t in left:
                yield t
            # 標準入力をIOから読み込む
            old_stdin = sys.stdin
            sys.stdin = io.StringIO(sys.stdout.getvalue())
            self.readable = True
            # 標準出力の復帰
            sys.stdout = old_stdout
            right = self.__interpret_internal(ast.right)
            for t in right:
                yield t
            # 標準入力の復帰
            sys.stdin = old_stdin
        
        if type(ast) == NodeConcat:
            left = self.__interpret_internal(ast.left)
            for t in left:
                yield t
            right = self.__interpret_internal(ast.right)
            for t in right:
                yield t

def search_script(script_name:str) -> Optional[str]:
    '''
    scriptsディレクトリ内にあるスクリプトを検索する
    '''
    script_name += ".py"
    SEARCH_DIR = "./src/scripts"
    for root, _, files in os.walk(SEARCH_DIR):
        if script_name in files:
            return os.path.join(root, script_name)
    return None

def path2module(path:str) -> str:
    '''
    ファイルパスをモジュール名に変換する
    '''
    # ./ と .pyを取り除いて/を.で置換
    return path[2:].replace('/','.')[:-3]

if __name__ == '__main__':
    myshell = ShellBase()
    myshell.run()   
    
    