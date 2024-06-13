'''
    API通信の内容をキャッシュするためのモジュール
'''
import os

from typing import Optional, List
from openapi.openapi_client.models import ChannelList, Channel

CACHE_DIR = './cache'

class NoCacheException(Exception):
    '''
        キャッシュが存在しない場合の例外
    '''

#TODO Fatal Error
class ParseFailedException(Exception):
    '''
        パースに失敗した場合の例外
    '''

class APICache:
    '''
        ファイルシステムを使ったAPI Responseのキャッシュを管理するクラス
    '''
    def __init__(self):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
    def __get(self, key: str) -> Optional[str]:
        '''
            キャッシュから値を取得する
        '''
        try:
            with open(f"{CACHE_DIR}/{key}.json", 'r',encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def __set(self, key: str, value: str):
        '''
            キャッシュに値をセットする
        '''
        with open(f"{CACHE_DIR}/{key}.json", "w", encoding="utf-8") as f:
            f.write(value)

    def set_channels(self, channels: ChannelList):
        '''
            チャンネルリストをキャッシュする
        '''
        chnls = ""
        for chnl in channels.public:
            self.__set(chnl.id, chnl.to_json())
            chnls += chnl.id + ","
        chnls = chnls.rstrip(',')
        self.__set('channels', chnls)

    def get_channel_ids(self) -> Optional[List[str]]:
        '''
            キャッシュからチャンネルIDリストを取得する
        '''
        chnls = self.__get('channels')
        if chnls is None:
            return None
        return chnls.split(',')

    def set_channel(self, channel: Channel):
        '''
            チャンネルをキャッシュする
        '''
        self.__set(channel.id, channel.to_json())
        chnls = self.__get('channels')
        if chnls is None:
            chnls = ""
        #TODO 重複チェック
        chnls += "," + channel.id
        self.__set('channels', chnls)

    def get_channel(self, channel_id: str) -> Channel:
        '''
            チャンネルを取得する
        '''
        chnl_raw = self.__get(channel_id)
        if chnl_raw is None:
            raise NoCacheException("the channel is not cached")
        chnl = Channel.from_json(chnl_raw)
        if chnl is None:
            raise ParseFailedException("failed to parse channel")
        return chnl
