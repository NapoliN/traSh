"""usermod: ユーザ情報を変更します"""

import argparse
import sys
from typing import Optional

from src.shell.session import Session
from src.shell.environment import Environment
from src.services.user_service import UserService
from src.services.channel_service import ChannelService

def usermod(new_username:Optional[str], new_home_directory:Optional[str]):
    """
        usermod: ユーザ情報を変更します
        Args:
            username: ユーザ名
            new_name: 新しいユーザ名
            new_home_directory: 新しいホームディレクトリ
    """
    session = Session()
    session.load_session()
    user_service = UserService(session=session)
    channel_service = ChannelService(session=session)
    env = Environment()
    _usermod(user_service, channel_service,env,new_username, new_home_directory)
    
def _usermod(user_service: UserService,channel_service: ChannelService, env:Environment, new_name:Optional[str], new_home_directory:Optional[str]):
    #TODO エラーハンドリング
    if new_name is not None:
        user_service.change_displayname(new_name)
        sys.stderr.write(f"表示名を @{new_name} に変更しました。\n")
    if new_home_directory is not None:
        current_channel_id = env.current_channel_id
        channel_id = channel_service.convert_path2idperfect(current_channel_id, new_home_directory)
        if channel_id is None:
            sys.stderr.write("チャンネルが見つかりませんでした。\n")
            return
        user_service.change_home_channel(channel_id)
        #TODO 新しいホームチャンネルのパスを絶対パスで表示する
        sys.stderr.write(f"ホームチャンネルを '{new_home_directory}' に変更しました。\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l",dest="new_name")
    parser.add_argument("-d",dest="new_home_directory")
    args = parser.parse_args()
    new_name = args.new_name
    new_home_directory = args.new_home_directory
    if new_name is None and new_home_directory is None:
        parser.print_help()
        sys.exit(0)
        
    usermod(new_name, new_home_directory)
