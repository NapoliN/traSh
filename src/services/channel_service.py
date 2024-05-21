import dataclasses
from typing import Optional

from openapi.openapi_client.api import ChannelApi, UserApi
from openapi_client.models.channel_list import ChannelList
from src.shell.session import Session

class ChannelService:
    '''
        チャンネル周りの操作のwrapper
    '''
    @dataclasses.dataclass
    class Message:
        '''
            メッセージ表示用のデータクラス
        '''
        username:str
        content:str
        created_at:str

    def __init__(self, session: Session):
        self.session = session
        self.channel_api = ChannelApi(api_client=session.client)
        # cache
        self.channels: Optional[ChannelList] = None

    def get_full_channel_path(self, channel_id:str) -> str:
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        if chnl.parent_id is None:
            return "#" + chnl.name
        else:
            return self.get_full_channel_path(chnl.parent_id) + "/" + chnl.name

    def search_channel_by_path(self, current_channel_id: str, path_:str) -> Optional[str]:
        # argを/で分割
        paths = path_.split("/")

        tmp_channel = current_channel_id

        if paths[0][0] == "#":
            root = paths[0][1:]
            root_id = self.search_channel(root, is_root=True)
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
                channel_id = ChannelService(self.session).search_channel(path,parent_id=tmp_channel)
                if channel_id is None:
                    return None
                else:
                    tmp_channel = channel_id
                    #self.prompt = f"({ChannelService(self.session).get_full_channel_path(channel_id)}):"
        return tmp_channel

    def search_channel(self, channel_name:str, parent_id:Optional[str]=None, child_id:Optional[str]=None, is_root:bool=False) -> Optional[str]:
        #TODO ネストしたチャンネルの検索
        if self.channels is None:
            self.channels = self.channel_api.get_channels()
        for chnl in self.channels.public:
            if chnl.name == channel_name and (parent_id is None or chnl.parent_id == parent_id) and (child_id is None or chnl.id == child_id) and (not is_root or chnl.parent_id is None):
                return chnl.id
        return None

    def print_channel_tree(self, channel_id:str, recursive:bool=False, archived:bool=False):
        self.__print_channel_tree(channel_id, 0, recursive, archived=archived)

    def __print_channel_tree(self, channel_id:str, depth:int, recrusive:bool, archived:bool):
        chnl = self.channel_api.get_channel(channel_id=channel_id)
        # flag archivedがないとき、アーカイブ済みのチャンネルは無視する
        if(not archived and chnl.archived):
            return
        print("--"*depth + chnl.name)
        if not recrusive and depth >= 1:
            return
        for child in chnl.children:
            self.__print_channel_tree(child, depth+1, recrusive, archived)

    def get_messages(self, channel_id:str, limit=10):
        messages = self.channel_api.get_messages(channel_id=channel_id,limit=limit)
        user_api = UserApi(api_client=self.session.client)

        return [self.Message(username=user_api.get_user(msg.user_id).name, content=msg.content, created_at=msg.created_at.strftime("%Y-%d-%m %H:%M:%S")) for msg in messages]