'''
シェルを提供するモジュール
'''
import sys
import io
import os
from typing import List, Optional, Generator, Tuple
from .cmd_parser import parse_input, TokenType
from .ast_ import ASTBuilder, Node, NodeCommand, NodePipe, NodeRedirect, NodeAnd, NodeOr, NodeConcat

import subprocess
                
class MyShell():
    '''
        シェルを提供するクラス
    '''
    def __init__(self):
        self.readable = False
        pass
    
    def run(self):
        while True:
            cmd = input('>>> ')
            if cmd == 'exit':
                break
            tokens = parse_input(cmd)
            ast = ASTBuilder().build_ast(tokens)
            self.__interpret(ast)
        pass
    
    def __interpret(self, ast:Node):
        '''
            ASTに従ってコマンドを実行する
        '''
        generator = self.__interpret_internal(ast)
        for cmd, args in generator:
            input_: Optional[str] = None
            if self.readable:
                input_ = sys.stdin.read()
                self.readable = False
            script_path = search_script(cmd)
            if script_path is not None:
                # src/scripts下にスクリプトがあるならそれを実行
                child = subprocess.run(['python', script_path, *args],encoding='utf-8',input=input_,stdout=subprocess.PIPE)           
            else:
                # なければ通常のコマンドを実行
                child = subprocess.run([cmd, *args],encoding='utf-8',input=input_,stdout=subprocess.PIPE)
                
            sys.stdout.write(child.stdout)
        pass

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

if __name__ == '__main__':
    myshell = MyShell()
    myshell.run()   
    
    