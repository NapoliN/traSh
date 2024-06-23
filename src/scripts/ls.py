'''
    lsコマンド: チャンネル一覧を表示します
'''
import argparse
import sys

from src.services.channel_service import ChannelService, IChannelService
from src.shell.session import Session
from src.shell.environment import Environment, IEnvironment

def ls(path:str, recursive:bool=False, archived:bool=False):
    """
        lsコマンド: チャンネル一覧を表示します
        Args:
            path: チャンネルのパス
            recursive: 再帰的に表示するかどうか
            archived: アーカイブ済みのチャンネルも表示するかどうか
    """
    session = Session()
    session.load_session()
    env = Environment()
    channel_service = ChannelService(session)
    _ls(path, channel_service, env, recursive=recursive, archived=archived)

def _ls(path:str, channel_service: IChannelService, env: IEnvironment, recursive:bool=False, archived:bool=False):
    # チャンネルのpathからidを取得
    channel_id = channel_service.convert_path2idperfect(env.current_channel_id, path)
    if channel_id is None:
        sys.stderr.write("チャンネルが見つかりませんでした。\n")
        return
    channel_service.print_channel_tree(channel_id, recursive=recursive, archived=archived)

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
