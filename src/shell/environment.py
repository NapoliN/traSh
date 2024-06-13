'''
    環境変数を管理するクラス
'''
import os
from abc import ABCMeta, abstractmethod

class IEnvironment(metaclass=ABCMeta):
    '''
        環境変数を管理するクラスのインターフェース
    '''
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
