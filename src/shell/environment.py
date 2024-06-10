import os
from typing import Optional, List
from abc import ABCMeta, abstractmethod
from openapi.openapi_client.models import ChannelList, Channel, User

class IEnvironment(metaclass=ABCMeta):
    @abstractmethod
    def set_current_channel(self, channel_id:str, channel_name: str):
        pass
    @property
    @abstractmethod
    def current_channel_id(self) -> str:
        pass
    @property
    @abstractmethod
    def current_channel_name(self) -> str:
        pass
    @abstractmethod
    def set_channels(self, channels: ChannelList):
        pass
    @abstractmethod
    def get_channel_ids(self) -> Optional[List[str]]:
        pass
    @abstractmethod
    def get_channel(self, channel_id:str) -> Channel:
        pass

class Environment(IEnvironment):
    '''
        シェル実行時の環境を管理するクラス
    '''
    
    def set_current_channel(self, channel_id:str, channel_name: str):
        '''
            現在いるチャンネルを設定する
        '''
        os.environ["QTRASH_CHANNEL"] = channel_id
        os.environ["QTRASH_CHANNEL_NAME"] = channel_name
    
    @property
    def current_channel_id(self):
        '''
            現在いるチャンネルのIDを取得する
            
            getterのみ、setはset_current_channelを経由して行う
        '''
        ch = os.environ.get("QTRASH_CHANNEL")
        if ch is None:
            raise Exception("No Channel Found. Please set TRAQ_CHANNEL environment variable.")
        return ch
        
    @property
    def current_channel_name(self) -> str:
        '''
            現在いるチャンネルの名称を取得する
            
            getterのみ、setはcurrent_channel_idを経由して行う
        '''
        name = os.environ.get("QTRASH_CHANNEL_NAME")
        if name is None:
            raise Exception("No Channel Found. Please set QTRASH_CHANNEL_NAME environment variable.")
        return name
        
    def set_channels(self, channels: ChannelList):
        '''
            チャンネルリストの情報を環境変数に設定する
        '''
        chnls = ""
        for chnl in channels.public:
            os.environ["QTRASH_CHANNEL_ID_" + chnl.id] = chnl.to_json()
            chnls += chnl.id + ";"
        chnls = chnls.rstrip(";")
        os.environ.setdefault("QTRASH_CHANNEL_LIST", chnls)
        
    def get_channel_ids(self) -> Optional[List[str]]:
        '''
            チャンネルIDのリストを取得する
        '''
        raw = os.environ.get("QTRASH_CHANNEL_LIST")
        if raw is None:
            return None
        # raw文字列をセミコロン区切りでパース
        return raw.split(";")

    def get_channel(self, channel_id:str) -> Channel:
        '''
            チャンネルIDからチャンネル名を取得する
        '''
        row = os.environ.get("QTRASH_CHANNEL_ID_" + channel_id)
        if row is None:
            raise Exception("Channel Not Found")
        chnl = Channel.from_json(row)
        if chnl is None:
            raise Exception("Parse Error")
        return chnl