import argparse

from src.services.channel_service import ChannelService
from src.session import Session
from src.environment import Environment

def cat(arg: str):
    """catコマンド: チャンネルのメッセージを表示します"""
    session = Session()
    session.load_session()
    env = Environment()
    channel_service = ChannelService(session)
    
    if arg == "":
        # current_channelのメッセージを表示
        messages = channel_service.get_messages(env.current_channel_id)
        for msg in messages:
            print(f"{msg.username}({msg.created_at}): {msg.content}")
    else:
        pass
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arg", default="")
    args = parser.parse_args()
    arg:str = args.arg
    cat(arg)