import argparse
from src.services.channel_service import ChannelService
from src.session import Session
from src.environment import Environment

def ls(path:str, recursive:bool=False, all:bool=False):
    """lsコマンド: チャンネル一覧を表示します"""
    
    session = Session()
    session.load_session()
    channel_service = ChannelService(session)
    env = Environment()
    
    
    # チャンネルのpathからidを取得
    channel_id = channel_service.search_channel_by_path(env.current_channel_id, path)
    if channel_id is None:
        print("チャンネルが見つかりませんでした")
        return
    channel_service.print_channel_tree(channel_id, recursive=recursive, archived=all)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default=".")
    parser.add_argument("-R","--recursive",action="store_true")
    parser.add_argument("-a","--all",action="store_true")
    args = parser.parse_args()
    flag_recursive = args.recursive
    flag_all = args.all
    path:str = args.path
    ls(path,flag_recursive, flag_all)