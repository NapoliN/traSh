'''
    headコマンド: チャンネルのメッセージを新しい順に表示します
'''
import argparse
from typing import List
import sys

from src.services import ChannelService, MessageService
from src.shell.session import Session
from src.shell.environment import Environment

def cat(channels: List[str], number:int):
    """
        headコマンド: チャンネルのメッセージを表示します
    """
    session = Session()
    session.load_session()
    env = Environment()
    message_service = MessageService(session)

    for channel_path in channels:
        channel_id = ChannelService(session).convert_path2idperfect(env.current_channel_id, channel_path)
        if channel_id is None:
            sys.stderr.write(f"チャンネル{channel_path}が見つかりませんでした。\n")
            continue
        messages = message_service.get_messages(channel_id,limit=number)
        for msg in reversed(messages):
            print(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("channels", nargs="+",default="")
    parser.add_argument("-n","--number", type=int, default=10)
    args = parser.parse_args()
    channels:List[str] = args.channels
    number= args.number
    cat(channels, number)
