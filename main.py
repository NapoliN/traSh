'''
mainモジュール
'''
import argparse
import cmd
import dataclasses
import getpass
import re
from typing import Optional

import certifi
from openapi_client import api_client
from openapi_client.models import PostLoginRequest
from openapi_client.models.channel_list import ChannelList

from openapi.openapi_client.api import (AuthenticationApi, ChannelApi, MeApi,
                                        UserApi)

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
    '''
        ログインに失敗したときの例外
    '''


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
            if res.status_code != 204:
                raise LoginFailException("IDもしくはパスワードが違います")
        except Exception as e:
            raise LoginFailException("apiに接続できませんでした。") from e
        assert res.headers is not None

        # cookieからセッションIDをもってきて設定する
        cookie = res.headers["Set-Cookie"]
        session = re.match(r"(r_session=.*?);", cookie)
        if session is None:
            raise Exception("セッションIDが取得できませんでした。")
        self.client.cookie = session.group(1)

        me_api = MeApi(api_client=self.client)
        user_detail = me_api.get_me()
        if user_detail.home_channel is None:
            raise Exception("ホームチャンネルが取得できませんでした")
        else:
            self.current_channel = user_detail.home_channel

        print(f"{TRASH}\ntraQ閲覧用対話型シェル、traShへようこそ、{user_detail.name}さん！")

    def try_exit(self):
        '''
            ログアウトを試行する
        '''
        auth_api = AuthenticationApi(api_client=self.client)
        res = auth_api.logout_with_http_info()
        if res.status_code != 204:
            raise Exception("ログアウトに失敗しました")
        print("ログアウトしました。")
        exit(0)

class CustomShell(cmd.Cmd):
    '''
        シェルエミュレータ
        do_xxでコマンドxxを追加する
    '''
    def __init__(self,session: Session):
        super().__init__()
        self.session = session
        assert self.session.current_channel is not None
        self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"

    def do_cd(self, arg: str):
        """cdコマンド: チャンネルを移動します"""
        channel_id = ChannelService(self.session).search_channel_by_path(arg)
        if channel_id is None:
            print("チャンネルが見つかりませんでした")
            return
        self.session.current_channel = channel_id
        self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"

    def do_ls(self, arg:str):
        """lsコマンド: チャンネル一覧を表示します"""
        assert self.session.current_channel is not None
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
        if channel_id is None:
            print("チャンネルが見つかりませんでした")
            return
        ChannelService(self.session).print_channel_tree(channel_id, recursive=flag_recursive, archived=flag_all)

    def do_cat(self, arg):
        """catコマンド: チャンネルのメッセージを表示します"""
        if arg == "":
            # current_channelのメッセージを表示
            messages = ChannelService(self.session).get_messages(self.session.current_channel)
            for msg in messages:
                print(f"{msg.username}({msg.created_at}): {msg.content}")
        else:
            pass

    def do_exit(self, _):
        """exitコマンド: シェルを終了します"""
        self.session.try_exit()

if __name__ == "__main__":
    ses = Session()
    print("traQにログインします。")
    while True:
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
