'''
    チャンネル取得関連のサービスクラス
'''
from typing import Optional, List
from abc import ABCMeta, abstractmethod

from openapi.openapi_client.api import ChannelApi
from openapi.openapi_client.models import ChannelList, Channel, PostChannelRequest
from src.shell.session import Session
from src.shell.environment import Environment
from src.shell.api_cache import APICache, NoCacheException

class IChannelService(metaclass=ABCMeta):
    '''
        チャンネル取得関連のサービスクラスのインターフェース
    '''
    @abstractmethod
    def get_channel_name(self, channel_id:str) -> str:
        pass
    @abstractmethod
    def create_channel(self, name: str, parent_id: str) -> None:
        pass
    @abstractmethod
    def convert_id2fullpath(self, channel_id:str) -> str:
        pass
    @abstractmethod
    def convert_path2idprefix(self, current_channel_id: str, path_:str) -> List[str]:
        pass
    @abstractmethod
    def convert_path2idperfect(self, current_channel_id: str, path_:str) -> Optional[str]:
        pass
    @abstractmethod
    def print_channel_tree(self, channel_id:str, recursive:bool=False, archived:bool=False):
        pass

class ChannelService(IChannelService):
    '''
        チャンネル取得関連のサービスクラス
    '''
    def __init__(self, session: Session):
        self.session = session
        self.channel_api = ChannelApi(api_client=session.client)
        self.env = Environment()
        self.cache = APICache() #TODO あとで隠蔽する

    @property
    def channels(self) -> ChannelList:
        channel_ids = self.cache.get_channel_ids()
        if channel_ids is None:
            chnls = self.channel_api.get_channels()
            self.cache.set_channels(chnls)
            return chnls

        chnl_list: List[Channel] = []        
        for channel_id in channel_ids:
            chnl = self.get_channel(channel_id=channel_id)
            chnl_list.append(chnl)
        return ChannelList(public=chnl_list)

    def get_channel(self, channel_id:str) -> Channel:
        '''
            チャンネルIDからチャンネルを取得する
            
            Args:
                channel_id: チャンネルID
        '''

        try:
            chnl = self.cache.get_channel(channel_id=channel_id)
        except NoCacheException:
            chnl = self.channel_api.get_channel(channel_id=channel_id)
            self.cache.set_channel(chnl)
        return chnl

    def get_channel_name(self, channel_id:str) -> str:
        '''
            チャンネルIDからチャンネル名を取得する
            
            Args:
                channel_id: チャンネルID
        '''

        return self.get_channel(channel_id=channel_id).name

    def convert_id2fullpath(self, channel_id:str) -> str:
        '''
            チャンネルIDをチャンネルへのフルパスに変換する
            
            Args:
                channel_id: チャンネルID
        '''
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        if chnl.parent_id is None:
            return "#" + chnl.name
        else:
            return self.convert_id2fullpath(chnl.parent_id) + "/" + chnl.name

    def convert_path2idprefix(self, current_channel_id: str, path_:str) -> List[str]:
        '''
            パスからチャンネルIDを前方一致で検索し、候補を返す
        '''
        return self.__convert_path2id(current_channel_id, path_, prefix_match=True)

    def convert_path2idperfect(self, current_channel_id: str, path_:str) -> Optional[str]:
        '''
            パスからチャンネルIDを完全一致で取得する
        '''
        match = self.__convert_path2id(current_channel_id, path_, prefix_match=False)
        if len(match) == 1:
            return match[0]
        elif len(match) == 0:
            return None
        else:
            raise Exception("FatalError: 複数のチャンネルがマッチしました")
    
    def __convert_path2id(self, current_channel_id: str, path_:str, prefix_match:bool = False) -> List[str]:
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
            #TODO ルートでのprefix searchの実装
            root = paths[0][1:]
            root_ids = self.search_name(root, is_root=True)
            if not root_ids:
                return []
            tmp_channel = root_ids[0]
            paths = paths[1:]

        for i, name in enumerate(paths):
            if name == "" or name == ".":
                continue
            elif name == "..":
                chnl = self.get_channel(channel_id=tmp_channel)
                if chnl.parent_id is None:
                    return []
                else:
                    tmp_channel = chnl.parent_id
                    #self.prompt = f"({ChannelService(self.session).get_full_channel_path(self.session.current_channel)}):"
            else:
                # 子チャンネルを検索
                if prefix_match and i == len(paths) - 1:
                    return self.search_name_with_parent(name,parent_id=tmp_channel, prefix_match=True)
                else:
                    candidates = self.search_name_with_parent(name,parent_id=tmp_channel, prefix_match=False)
                    if not candidates:
                        return []
                    else:
                        tmp_channel = candidates[0]
        return [tmp_channel]

    def create_channel(self, name: str, parent_id: str) -> None:
        '''
            チャンネルを作成する
            呼び出すときは409エラーが起きないことを期待する
        '''
        request = PostChannelRequest(name=name, parent=parent_id)
        chnl = self.channel_api.create_channel(request)
        new_parent = self.channel_api.get_channel(parent_id)
        # キャッシュ上のチャンネル情報の更新
        self.cache.set_channel(chnl)
        self.cache.set_channel(new_parent)

    def search_name_with_parent(self, channel_name: str, parent_id: str, prefix_match: bool = False) -> List[str]:
        '''
            特定の親チャンネルを持つチャンネル名からチャンネルIDを取得する
        '''
        parent_chnl = self.get_channel(parent_id)
        candidates = []
        for child_id in parent_chnl.children:
            child_chnl = self.get_channel(child_id)
            if prefix_match:
                if child_chnl.name.startswith(channel_name):
                    candidates.append(child_id)
            else:
                if child_chnl.name == channel_name:
                    return [child_id]
        return candidates

    def search_name(self, channel_name:str, child_id:Optional[str]=None, is_root:bool=False, prefix_match: bool = False) -> List[str]:
        '''
            特定の相対位置関係をもつチャンネル名からチャンネルIDを取得する
        '''
        candidates = []
        #TODO ネストしたチャンネルの検索
        for chnl in self.channels.public:
            # 子に向かって検索 -> 親のIDが一致
            # 親に向かって検索 -> 子のIDが一致
            # ルートから探索 -> 親IDがない
            if (child_id is None or chnl.id == child_id) and (not is_root or chnl.parent_id is None):
                if prefix_match:
                    if chnl.name.startswith(channel_name):
                        candidates.append(chnl.id)
                else:
                    if chnl.name == channel_name:
                        return [chnl.id]
        if prefix_match:
            #candidates.clear()
            return [] #ここはout
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