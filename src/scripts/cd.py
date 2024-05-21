import argparse

from src.services.channel_service import ChannelService
from src.shell.session import Session
from src.shell.environment import Environment

def cd(path:str):
    """
        cdコマンド: チャンネルを移動します
    """
    session = Session()
    session.load_session()
    env = Environment()
    channel_service = ChannelService(session)
    
    channel_id = channel_service.convert_name2id(env.current_channel_id, path)
    if channel_id is None:
        print("チャンネルが見つかりませんでした")
        exit(1)
    channel_name = channel_service.convert_id2name(channel_id)
    env.set_current_channel(channel_id, channel_name)