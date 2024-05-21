import argparse

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
    args = parser.parse_args()
    arg:str = args.arg
    cat(arg)