import argparse

from src.services.channel_service import ChannelService, IChannelService
from src.shell.session import Session
from src.shell.environment import Environment, IEnvironment

def cd(path:str):
    """
        cdコマンド: チャンネルを移動します
    """
    session = Session()
    session.load_session()
    channel_service = ChannelService(session)
    env = Environment()
    _cd(path, channel_service, env)
    
def _cd(path: str, channel_service:IChannelService, env:IEnvironment):    
    channel_id = channel_service.convert_path2idperfect(env.current_channel_id, path)
    if channel_id is None:
        print("チャンネルが見つかりませんでした")
        exit(1)
    channel_fullpath = channel_service.convert_id2fullpath(channel_id)
    env.set_current_channel(channel_id, channel_fullpath)