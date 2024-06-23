'''mkdir:   チャンネルを作成します'''

import sys
import argparse

from src.services.channel_service import ChannelService, IChannelService
from src.shell.session import Session
from src.shell.environment import Environment, IEnvironment

def mkdir(name: str):
    '''
        mkdirコマンド:チャンネルを作成します
        現在は今のチャンネルの子チャンネルに作ることしかできません
        Args:
            name: 作成するチャンネル名
    '''
    session = Session()
    session.load_session()
    env = Environment()
    channel_service = ChannelService(session)
    _mkdir(name, channel_service, env)
    
def _mkdir(name: str, channel_service: IChannelService, env: IEnvironment):
    '''
        mkdirコマンド:チャンネルを作成します
        Args:
            name: 作成するチャンネル名
            channel_service: チャンネルサービス
            env: 環境
    '''
    
    print(channel_service.convert_path2idperfect(env.current_channel_id, name),file=sys.stderr)
    # 重複チェック
    if channel_service.convert_path2idperfect(env.current_channel_id, name) is not None:
        sys.stderr.write("同名のチャンネルが既に存在します。\n")
        return
    
    # 最終確認
    while True:
        sys.stderr.write(f"実行すると{name}が新たに作成されます。(作成後のチャンネルの削除や移動、チャンネル名の変更はできません。)よろしいですか？(y/n):")
        ans = input()
        if ans == "y" or ans == "yes":
            break
        elif ans == "n" or ans == "no":
            return
    try:    
        channel_service.create_channel(name, env.current_channel_id)
    except Exception as e:
        sys.stderr.write("チャンネルの作成に失敗しました。\n")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default=".")
    args = parser.parse_args()
    mkdir(args.path)
