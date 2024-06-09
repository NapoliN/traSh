import sys
import termios
import tty
import select
from typing import List


def clear_last_n_chars(n: int):
    """
        標準出力から最後のn文字を消去する
    """
    print('\b \b' * n, end='', flush=True)

class InputReader():
    '''
        標準入力を読み込むクラス
        tabキーで補完を行えるようにする
    '''
    def __init__(self) -> None:
        self.candidate: List[str] = []
        self.input_buffer: List[str] = []

    def read(self, prompt: str) -> str:
        old_settings = termios.tcgetattr(sys.stdin)
        cmd = self.__read(prompt, "")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return cmd
    
    def completion(self, prefix: str) -> List[str]:
        '''
            補完候補を返すhook関数
        '''
        return []
        
    def __read(self, prompt: str, init: str) -> str:
        try:
            print(prompt, end=' ', flush=True)
            print(init, end='', flush=True)
            tty.setcbreak(sys.stdin.fileno())  # 生入力モードに設定
            while True:
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    char = sys.stdin.read(1)
                    if char == '\n' or char == '\r': # 入力の終了
                        print()
                        cmd = ''.join(self.input_buffer)
                        self.input_buffer.clear()
                        self.candidate.clear()
                        return cmd
                    
                    elif char == '\b' or char == '\x7f': # 入力中の文字消去
                        if self.input_buffer:
                            self.input_buffer.pop()
                            clear_last_n_chars(1)
                            
                    elif char == '\t': # 補完処理
                        if self.input_buffer:
                            input_ = ''.join(self.input_buffer)
                            splited = input_.lstrip().split()
                            if len(splited) < 1: #TODO コマンド補完への対応
                                continue
                            prefix =  splited[-1]
                            self.candidate = self.completion(prefix)
                            if(not self.candidate):
                                continue
                            elif len(self.candidate) == 1:
                                n_prefix = len(prefix)
                                clear_last_n_chars(n_prefix)
                                self.input_buffer = self.input_buffer[:-n_prefix] + list(self.candidate[0])
                                print(*self.candidate, end='', flush=True)
                                self.candidate.clear()
                            else:
                                print()
                                for c in self.candidate:
                                    print(c, end=' ')
                                print()
                                return self.__read(prompt, input_)
                    else:
                        self.input_buffer.append(char)
                        print(char, end='', flush=True)
        except KeyboardInterrupt as e:
            raise e 

if __name__ == "__main__":
    reader = InputReader()

    input_ = reader.read(">>")
    print(input_)
