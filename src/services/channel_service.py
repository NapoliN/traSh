import dataclasses
from typing import Optional

from openapi.openapi_client.api import ChannelApi, UserApi
from openapi_client.models.channel_list import ChannelList
from src.shell.session import Session

class ChannelService:
    '''
        チャンネル取得関連のサービスクラス
    '''

    def __init__(self, session: Session):
        self.session = session
        self.channel_api = ChannelApi(api_client=session.client)
        # cache
        self.channels: Optional[ChannelList] = None

    def convert_id2name(self, channel_id:str) -> str:
        '''
            チャンネルIDをパス名に変換する
            
            Args:
                channel_id: チャンネルID
        '''
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        if chnl.parent_id is None:
            return "#" + chnl.name
        else:
            return self.convert_id2name(chnl.parent_id) + "/" + chnl.name

    def convert_name2id(self, current_channel_id: str, path_:str) -> Optional[str]:
        '''
            パス名をチャンネルIDに変換する
            
            #から始まるときはrootから探索
            
            そうでなければcurrent_channel_idからの相対で探索
            
            Args:
                current_channel_id: 現在のチャンネルID
                path_: 探索したいパス
        '''
        # argを/で分割
        paths = path_.split("/")

        tmp_channel = current_channel_id

        if paths[0][0] == "#":
            root = paths[0][1:]
            root_id = self.__convert_name2id_internal(root, is_root=True)
            if root_id is None:
                return None
            tmp_channel = root_id
            paths = paths[1:]

        for path in paths:
            if path == "" or path == ".":
                continue
            elif path == "..":
                chnl = ChannelService(self.session).channel_api.get_channel(channel_id=tmp_channel)
                if chnl.parent_id is None:
                    return None
                else:
                    tmp_channel = chnl.parent_id
                    #self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"
            else:
                # 子チャンネルを検索
                channel_id = ChannelService(self.session).__convert_name2id_internal(path,parent_id=tmp_channel)
                if channel_id is None:
                    return None
                else:
                    tmp_channel = channel_id
                    #self.prompt = f"({ChannelService(self.session).get_full_channel_path(channel_id)}):"
        return tmp_channel

    def __convert_name2id_internal(self, channel_name:str, parent_id:Optional[str]=None, child_id:Optional[str]=None, is_root:bool=False) -> Optional[str]:
        '''
            convert_name2idの内部実装
        '''
        #TODO ネストしたチャンネルの検索
        if self.channels is None:
            self.channels = self.channel_api.get_channels()
        for chnl in self.channels.public:
            if chnl.name == channel_name and (parent_id is None or chnl.parent_id == parent_id) and (child_id is None or chnl.id == child_id) and (not is_root or chnl.parent_id is None):
                return chnl.id
        return None

    def print_channel_tree(self, channel_id:str, recursive:bool=False, archived:bool=False):
        '''
            チャンネルを木構造で標準出力に表示する
            
            Args:
                channel_id: チャンネルID
                recursive: 子チャンネルを再帰的に表示するかどうか
                archived: アーカイブ済みのチャンネルも表示するかどうか
        '''
        self.__print_channel_tree(channel_id, 0, recursive, archived=archived)

    def __print_channel_tree(self, channel_id:str, depth:int, recrusive:bool, archived:bool):
        '''
            prent_channel_treeの内部実装
        '''
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        # flag archivedがないとき、アーカイブ済みのチャンネルは無視する
        if(not archived and chnl.archived):
            return
        print("--"*depth + chnl.name)
        if not recrusive and depth >= 1:
            return
        for child in chnl.children:
            self.__print_channel_tree(child, depth+1, recrusive, archived)