import dataclasses
from typing import Optional, List

from openapi.openapi_client.api import ChannelApi
from openapi.openapi_client.models import ChannelList
from src.shell.session import Session
from src.shell.environment import Environment

class ChannelService:
    '''
        チャンネル取得関連のサービスクラス
    '''

    def __init__(self, session: Session):
        self.session = session
        self.channel_api = ChannelApi(api_client=session.client)
        self.__channels: Optional[ChannelList] = None
        
    @property
    def channels(self) -> ChannelList:
        if self.__channels is not None:
            return self.__channels
        env = Environment()
        chnls_str = env.channel_list
        if chnls_str is None:
            chnls_loaded = self.channel_api.get_channels()
            self.__channels = chnls_loaded
            env.channel_list = chnls_loaded.to_json()
            return chnls_loaded       
        chnls = ChannelList.from_json(chnls_str)
        if chnls is None:
            raise Exception()
        self.__channels = chnls
        return chnls

    def get_channel_name(self, channel_id:str) -> str:
        '''
            チャンネルIDからチャンネル名を取得する
            
            Args:
                channel_id: チャンネルID
        '''
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        return chnl.name
    
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

    def convert_name2idprefix(self, current_channel_id: str, path_:str) -> List[str]:
        return self.convert_name2id(current_channel_id, path_, prefix_match=True)
    
    def convert_name2idperfect(self, current_channel_id: str, path_:str) -> Optional[str]:
        match = self.convert_name2id(current_channel_id, path_, prefix_match=False)
        if len(match) == 1:
            return match[0]
        elif len(match) == 0:
            return None
        else:
            raise Exception("FatalError: 複数のチャンネルがマッチしました")
    
    def convert_name2id(self, current_channel_id: str, path_:str, prefix_match:bool = False) -> List[str]:
        '''
            パス名をチャンネルIDに変換する
            
            #から始まるときはrootから探索
            
            そうでなければcurrent_channel_idからの相対で探索
            
            Args:
                current_channel_id: 現在のチャンネルID
                path_: 探索したいパス
                prefix_match: 前方一致検索を行うかどうか
        '''
        # argを/で分割
        paths = path_.split("/")

        tmp_channel = current_channel_id

        if paths[0][0] == "#":
            root = paths[0][1:]
            root_ids = self.__convert_name2id_internal(root, is_root=True)
            if not root_ids:
                return []
            tmp_channel = root_ids[0]
            paths = paths[1:]

        for i, path in enumerate(paths):
            if path == "" or path == ".":
                continue
            elif path == "..":
                chnl = self.channel_api.get_channel(channel_id=tmp_channel)
                if chnl.parent_id is None:
                    return []
                else:
                    tmp_channel = chnl.parent_id
                    #self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"
            else:
                # 子チャンネルを検索
                if prefix_match and i == len(paths) - 1:
                    return self.__convert_name2id_internal(path,parent_id=tmp_channel, prefix_match=True)
                else:
                    candidates = self.__convert_name2id_internal(path,parent_id=tmp_channel, prefix_match=False)
                    if not candidates:
                        return []
                    else:
                        tmp_channel = candidates[0]
        return [tmp_channel]

    def __convert_name2id_internal(self, channel_name:str, parent_id:Optional[str]=None, child_id:Optional[str]=None, is_root:bool=False, prefix_match: bool = False) -> List[str]:
        '''
            convert_name2idの内部実装
        '''
        candidates = []
        #TODO ネストしたチャンネルの検索
        for chnl in self.channels.public:
            # 子に向かって検索 -> 親のIDが一致
            # 親に向かって検索 -> 子のIDが一致
            # ルートから探索 -> 親IDがない
            if (parent_id is None or chnl.parent_id == parent_id) and (child_id is None or chnl.id == child_id) and (not is_root or chnl.parent_id is None):
                if prefix_match:
                    if chnl.name.startswith(channel_name):
                        candidates.append(chnl.id)
                else:
                    return [chnl.id]
        return candidates

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