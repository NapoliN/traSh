import argparse
import os

from src.services import ChannelService, MessageService
from src.shell.session import Session
from src.shell.environment import Environment

def cat(arg: str):
    """
        catコマンド: チャンネルのメッセージを表示します
    """
    session = Session()
    session.load_session()
    env = Environment()
    message_service = MessageService(session)
    
    if arg == "":
        # current_channelのメッセージを表示
        messages = message_service.get_messages(env.current_channel_id)
        for msg in messages:
            print(msg)
    else:
        pass
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arg", default="")
    parser.add_argument("--system", action="store_true")
    args = parser.parse_args()
    arg:str = args.arg
    is_system:bool = args.system
    if is_system:
        os.execvp("cat",["cat", arg])
    cat(arg)