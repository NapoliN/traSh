'''uname:   ユーザ詳細情報を表示します'''

import argparse
import sys
from typing import Optional

from src.shell.session import Session
from src.shell.environment import Environment
from src.services.user_service import UserService
from src.services.channel_service import ChannelService

def uname(username: Optional[str] = None):
    session = Session()
    session.load_session()
    user_service = UserService(session=session)
    channel_service = ChannelService(session=session)
    env = Environment()
    _uname(user_service, channel_service, env, username)

def _uname(user_service: UserService, channel_service: ChannelService, env: Environment, username: Optional[str]):
    if username is None:
        raise NotImplementedError("username is required")
    username = username.lstrip("@")
    info = user_service.get_user_info(username)
    if info is None:
        sys.stderr.write(f"ユーザ {username} が見つかりませんでした。\n")
        return
    home_channel_path = None if info.home_channel is None else channel_service.convert_id2fullpath(info.home_channel)
    print(f"UserName:       {info.name}")
    print(f"DisplayName:    {info.display_name}")
    print(f"HomeChannel:    {home_channel_path}")
    print(f"Bio:", end="")
    bio_lines = info.bio.splitlines()
    if bio_lines:
        print(f"            {bio_lines[0]}")
        for line in bio_lines[1:]:
            print(f"                {line}")
    else:
        print()
    print(f"IsBot:          {info.bot}")
    print(f"LastLogin:      {info.last_online}")
    if info.groups:
        print(f"Groups:")
        for group in info.groups:
            group_name = user_service.get_group_name(group)
            print(f"    {group_name}")
    if info.tags:
        print(f"Tags:")
        for tag in info.tags:
            print(f"    {tag.tag}")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", nargs="?", default=None)
    args = parser.parse_args()
    username = args.username
    uname(username)