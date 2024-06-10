import getpass
from typing import List
import argparse
import sys

from .shell import ShellBase, ChanneiIO
from .session import Session
from .environment import Environment
from openapi.openapi_client.api.me_api import MeApi
from src.services import ChannelService, MessageService
from src.scripts.cd import cd
from src.shell.input_reader import InputReader

TRASH_LOGO = """
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMY<;?MMB"YYTT"HM#<;?TMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM#<;;;;?N;;;;;:;;;;;;;;jMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMM#MMMN+;;;;dmggggggJ;;;:;;TMM#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMM5;;?HMMe;;;;<;;;MMM8:;;+;;;?>;;dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MM5;;:;;<7M6;;;;;;+MM#;;:;TB<;;;;;:dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMg+<;:;;;;;;;jkMYYYTMQJ;;;;;:;:;;jjMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMNagJ<;;jM5;;;;;;;<dN/;;+jg;:<MMMMMMMMMMNg&+;;:;+jdMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#3<;;;;;;;<?TMMNdMMMMMNx;;:;<gMMMMMMMMMMMMMMMMMMMMMMMM
N;;;;?1?YTBqMD;;<jggJ;;;dNNMMMM>;;dMMMMMMMMMMM#;;:;;dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM>;;;;:;;;;;;;;:<6<MMMMMM@;;;;jMMMMMMMMMMMMMMMMMMMMMMMMM
N;;;;;;;;;;MMI;;MMMMMb;;JMP;;dMP;;dMMMMM#MMMMM3;;;;jMMMM6MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP;;;:;;:;;:;<dMNgJ;dMMMMM@;:;jMMMMMMMMMMMMMMMMMMMMMMMMMM
N;;:;j+j+jgMM[;;<TMM5;:;jM>;:dM3;;dMMMMM#;V""5;;:;:?TTT;+MMNa;;;:d#5<;:;?T#1MM#3;;;;;<dMI;;;gMN;;:;;;;:;;:<TMMMMMmMMMMM@;;;dMBC;:;:<?HMMMMMMMMMMMMMMMM
MMMMMM#86<;;dNJ;;;;;;;<jM3;;;7"z++MMMMMMM;;;;;;;;:;;++j;jMMM#:;;?>;;;:;:;;;dM8;;;;;jJ;;<5;;;MMMNJ;;:;;;:;;;;;?T"MMMMMMM@;;j5;:;;;:;;;;?MMMMMMMMMMMMMMM
MMBC;;;;;;;jg@TMgJ+++gT3;;:;:;;;:;7TMMMMM;j+e;:;;;<MMMMNJMMM#:;;;:;;:;;;:;jM#;;:;:;MMMp;;:;;MMMMMMNgJ+;;:;;:;;;;:;?TMMM@;:;;;;:;;;;;;;;dMMMMMMMMMMMMMM
MMs;;:;;+jMMC;;+ME<;M#;;;;uNJ:;;;;;jMMMMMWMM$;;:;:;MMMMMMMMMP;;:;;jiNNag+;dMI;;;:;;?MMMK;;:;MMMMMMMMMMMN+;;;:;;:;;;;;dMN;;:;:;;:;:;::;;jMMMMMMMMMMMMMM
MMMs;;jgMMB<;;;dM$;;JMp;:;?MMNe<;;jMMMMMMMMM;;;;;;;MMMMM#dMMP;;;:jMMMMMMMNMMI:;;;;;;;;:;;;;;MMMfHMMMMMMM@;:;;:;;;:;;;jMN:;;;<jgg+;;;;;<MMMMMMMMMMMMMMM
MMMMmMMMMC;;;;jMM;;;jMM2;:;<7MMMNdMMMMMMMMMM+;:;:;;<TY3;;?MMC;;:;dMMMMMMMMMMb;:;:;:;;:;;+;:;dMMN<;?TWHB5;;;:;;;:;;:;<dMN:;;:dMMMN;;:;<dMMMMMMMMMMMMMMM
MMMMMMM#;;;;;jMM@;;;<MMN+;;;;jMMMMMMMMMMMMMMN+;:;;;;;;;+J;MM<;;;;?MMMMMMMMMMMm<;;:;;:;jd3;;;dMMMKje+;;;;;:;;;;:;;;;jMMMN:;;;MMMM#;:;jMMMMMMMMMMMMMMMMM
MMMMMMMMNJ<;jMMMD;;;;dMMN<;jjMMMMMMMMMMMMMMMMMNJ+++jj&MMMNd5++++++jMMMMMMMMMMMMNJ++igMMNj&&ggNMMMdMMNgJJ+;:;:+++&NMMMMBI+++j&MM#1++j+ggMMMMMMMMMMMMMMM
MMMMMMMMMMMNMMMMe++++dMMMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
"""

class InputReaderForTraQ(InputReader):
    def __init__(self, session: Session):
        super().__init__()
        self.env = Environment()
        self.session = session
        
    def completion(self, prefix: str) -> List[str]:
        """
            チャンネル名の補完を行う
        """
        channel_service = ChannelService(self.session)
        current_id = self.env.current_channel_id
        candidates_id = channel_service.convert_path2idprefix(current_id, prefix)
        candidates_name = [channel_service.get_channel_name(ch_id) for ch_id in candidates_id]
        return candidates_name
        

class TraQShell(ShellBase):
    '''
    traQ用のシェル
    '''
    def __init__(self):
        super().__init__()
        self.prompt = 'traq> '
        self.session = Session()
        self.environment = Environment()
        self.input_reader = InputReaderForTraQ(session=self.session)

    def read(self) -> str:
        return self.input_reader.read(self.prompt)

    def start(self):
        '''
        
        '''
        # ログイン処理
        while True:
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            try:
                self.session.try_login(username, password)
                me_api = MeApi(api_client=self.session.client)
                user_detail = me_api.get_me()
                channel_service = ChannelService(self.session)
                if user_detail.home_channel is None:
                    raise Exception("ホームチャンネルが取得できませんでした")
                else:
                    channel_id = user_detail.home_channel
                    channel_name = channel_service.convert_id2fullpath(channel_id)
                    self.environment.set_current_channel(channel_id, channel_name)
                break
            except Exception as e:
                print(f'Login Failed: {e}')
        print(TRASH_LOGO)
        print("welcome to traSh'ell!")
        self.run()
        
    def preinput(self):
        self.prompt = f'{self.environment.current_channel_name}> '
        return super().preinput()
    
    def postcmd(self):
        # channelIOの処理
        if self.channelIOs:
            channel_service = ChannelService(self.session)
            message_service = MessageService(self.session)
            if self.outbuffer is None:
                raise Exception("Fatal Error: No output buffer found.")
            content = self.outbuffer.getvalue()
            for channelIO in self.channelIOs:
                if channelIO.type_ == ChanneiIO.Type.Out:
                    ch_name = channelIO.channel_name
                    current_channel_id = self.environment.current_channel_id
                    # ch_nameのチャンネルIDに書き込む
                    ch_id = channel_service.convert_path2idperfect(current_channel_id,ch_name)
                    if ch_id is None:
                        raise Exception("チャンネルが見つかりませんでした")
                    message_service.post_message(ch_id, content)
                    
            self.channelIOs.clear()
    
    def do_cd(self, args: List[str]):
        parser = argparse.ArgumentParser()
        parser.add_argument("path", default=".")
        parsed = parser.parse_args(args)
        path:str = parsed.path
        cd(path)
    
if __name__ == "__main__":
    shell = TraQShell()
    shell.start()
    # unreachable
    assert False