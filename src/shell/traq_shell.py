import getpass

from .shell import ShellBase
from .session import Session
from .environment import Environment
from openapi.openapi_client.api.me_api import MeApi
from ..services.channel_service import ChannelService

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

class TraQShell(ShellBase):
    '''
    traQ用のシェル
    '''
    def __init__(self):
        super().__init__()
        self.prompt = 'traq> '
        self.session = Session()
        self.environment = Environment()

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
                    channel_name = channel_service.get_full_channel_path(channel_id)
                    self.environment.set_current_channel(channel_id, channel_name)
                break
            except Exception as e:
                print(f'Login Failed: {e}')
        self.run()
        
    def preinput(self):
        self.prompt = f'{self.environment.current_channel_name}> '
        return super().preinput()
    
if __name__ == "__main__":
    shell = TraQShell()
    shell.start()
    # unreachable
    assert False