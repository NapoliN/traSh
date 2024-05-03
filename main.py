from typing import Optional
import cmd
from openapi.openapi_client.api import AuthenticationApi, MeApi, ChannelApi, UserApi

from openapi_client.models import PostLoginRequest
from openapi_client.models.channel_list import ChannelList
from openapi_client import api_client
import certifi

import re
import getpass
import argparse

import dataclasses


TRASH = """
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

class LoginFailException(Exception):
    pass
 
class Session:
    '''
        sessionクラス
    '''
    def __init__(self):
        self.session_id = None
        self.current_channel = None
    # sessionを保持するためのクライアントを作成
    client = api_client.ApiClient(configuration=api_client.Configuration(ssl_ca_cert=certifi.where()))

    current_channel:Optional[str] = None

    # ログインを試行する
    def try_login(self, username: str, password: str):
        '''
            ログイン用
        '''
        auth_api = AuthenticationApi(api_client=self.client)
        try:
            res = auth_api.login_with_http_info(post_login_request=PostLoginRequest(name=username, password=password))
            if(res.status_code != 204):
                raise LoginFailException("IDもしくはパスワードが違います")
        except Exception as e:
            raise LoginFailException("apiに接続できませんでした。") from e

        assert(res.headers is not None)
        
        # cookieからセッションIDをもってきて設定する
        cookie = res.headers["Set-Cookie"]
        session = re.match(r"(r_session=.*?);", cookie)
        if(session is None):
            raise Exception("セッションIDが取得できませんでした。")
        self.client.cookie = session.group(1)

        me_api = MeApi(api_client=self.client)
        user_detail = me_api.get_me()
        if(user_detail.home_channel is None):
            raise Exception("ホームチャンネルが取得できませんでした")
        else:
            self.current_channel = user_detail.home_channel
            self.current_channel_name = user_detail.name
        
        print(f"{TRASH}\ntraQ閲覧用対話型シェル、traShへようこそ、{user_detail.name}さん！")
        
    def try_exit(self):
        auth_api = AuthenticationApi(api_client=self.client)
        res = auth_api.logout_with_http_info()
        if(res.status_code != 204):
            raise Exception("ログアウトに失敗しました")
        print("ログアウトしました。")
        exit(0)
        
class ChannelService:
    @dataclasses.dataclass
    class Message:
        username:str
        content:str
        created_at:str
    
    def __init__(self, session: Session):
        self.session = session
        self.channel_api = ChannelApi(api_client=session.client)
        # cache
        self.channels: Optional[ChannelList] = None
    
    def get_full_channel_path(self, channel_id:str):
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        if chnl.parent_id is None:
            return "#" + chnl.name
        else:
            return self.get_full_channel_path(chnl.parent_id) + "/" + chnl.name
    
    def search_channel_by_path(self, path_:str) -> Optional[str]:
        assert(self.session.current_channel is not None)
        """cdコマンド: チャンネルを移動します"""
        # argを/で分割
        paths = path_.split("/")
        
        tmp_channel = self.session.current_channel
        
        if(paths[0][0] == "#"):
            root = paths[0][1:]
            root_id = self.search_channel(root, is_root=True)
            if(root_id is None):
                return None
            tmp_channel = root_id
            paths = paths[1:]
        
        for path in paths:
            if path == "" or path == ".":
                continue
            elif path == "..":
                chnl = ChannelService(self.session).channel_api.get_channel(channel_id=tmp_channel)
                if chnl.parent_id is None:
                    return None
                else:
                    tmp_channel = chnl.parent_id
                    #self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"
            else:
                # 子チャンネルを検索
                channel_id = ChannelService(self.session).search_channel(path,parent_id=tmp_channel)
                if channel_id is None:
                    return None
                else:
                    tmp_channel = channel_id
                    #self.prompt = f"({ChannelService(self.session).get_full_channel_path(channel_id)}):"
        return tmp_channel              
    
    def search_channel(self, channel_name:str, parent_id:Optional[str]=None, child_id:Optional[str]=None, is_root:bool=False) -> Optional[str]:
        #TODO ネストしたチャンネルの検索
        if(self.channels is None):
            self.channels = self.channel_api.get_channels()
        for chnl in self.channels.public:
            if chnl.name == channel_name and (parent_id is None or chnl.parent_id == parent_id) and (child_id is None or chnl.id == child_id) and (not is_root or chnl.parent_id is None):
                return chnl.id
        return None
    
    def print_channel_tree(self, channel_id:str, recursive:bool=False, archived:bool=False):
        self.__print_channel_tree(channel_id, 0, recursive, archived=archived)
    
    def __print_channel_tree(self, channel_id:str, depth:int, recrusive:bool, archived:bool):
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        # flag archivedがないとき、アーカイブ済みのチャンネルは無視する
        if(not archived and chnl.archived):
            return
        print("--"*depth + chnl.name)
        if not recrusive and depth >= 1:
            return
        for child in chnl.children:
            self.__print_channel_tree(child, depth+1, recrusive, archived)

    def get_messages(self, channel_id:str, limit=10):
        messages = self.channel_api.get_messages(channel_id=channel_id,limit=limit)
        user_api = UserApi(api_client=self.session.client)
        
        return [self.Message(username=user_api.get_user(msg.user_id).name, content=msg.content, created_at=msg.created_at.strftime("%Y-%d-%m %H:%M:%S")) for msg in messages]

class CustomShell(cmd.Cmd):
    def __init__(self,session: Session):
        super().__init__()
        self.session = session
        assert(self.session.current_channel is not None)
        self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"

    def do_cd(self, arg: str):
        """cdコマンド: チャンネルを移動します"""
        channel_id = ChannelService(self.session).search_channel_by_path(arg)
        if(channel_id is None):
            print("チャンネルが見つかりませんでした")
            return
        self.session.current_channel = channel_id
        self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"

    def do_ls(self, arg:str):
        """lsコマンド: チャンネル一覧を表示します"""
        assert(self.session.current_channel is not None)
        parser = argparse.ArgumentParser()
        parser.add_argument("path", default=".")
        parser.add_argument("-R","--recursive",action="store_true")
        parser.add_argument("-a","--all",action="store_true")
        args = parser.parse_args(arg.split())
        flag_recursive = args.recursive
        flag_all = args.all
        path:str = args.path
        # チャンネルのpathからidを取得
        channel_id = ChannelService(self.session).search_channel_by_path(path)
        if(channel_id is None):
            print("チャンネルが見つかりませんでした")
            return
        ChannelService(self.session).print_channel_tree(channel_id, recursive=flag_recursive, archived=flag_all)
        
    def do_cat(self, arg):
        """catコマンド: チャンネルのメッセージを表示します"""
        if(arg == ""):
            # current_channelのメッセージを表示
            messages = ChannelService(self.session).get_messages(self.session.current_channel)
            for msg in messages:
                print(f"{msg.username}({msg.created_at}): {msg.content}")
        else:
            pass
        
    def do_exit(self, args):
        """exitコマンド: シェルを終了します"""
        self.session.try_exit()
        
if __name__ == "__main__":
    ses = Session()
    print("traQにログインします。")
    while(True):
        # 成功するまでログインを試行
        username = input("username:")
        password = getpass.getpass(prompt="password:")
        try:
            ses.try_login(username, password)
            break
        except Exception as e:
            print(e)
            continue
        
    CustomShell(ses).cmdloop()