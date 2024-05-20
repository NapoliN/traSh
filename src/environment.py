import os
from src.services.channel_service import ChannelService
from src.session import Session

class Environment:
    '''
        シェル実行時の環境を管理するクラス
    '''
    
    def set_current_channel(self, channel_id:str, channel_name: str):
        '''
            現在いるチャンネルを設定する
        '''
        os.environ.setdefault("QTRASH_CHANNEL", channel_id)
        os.environ.setdefault("QTRASH_CHANNEL_NAME", channel_name)
    
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
