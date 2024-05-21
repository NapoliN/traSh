import dataclasses
import datetime
from openapi.openapi_client import ChannelApi, UserApi
from openapi.openapi_client.models import PostMessageRequest
from src.shell.session import Session

@dataclasses.dataclass
class Message:
    '''
        メッセージ表示用のデータクラス
    '''
    username:str
    content:str
    created_at: datetime.datetime
    def __str__(self):
        return f"{self.username}({self.created_at.strftime("%Y/%m/%D %H:%M:%S")}): {self.content}"

class MessageService():
    '''
        メッセージ取得/送信周りのサービスクラス
    '''
    def __init__(self, session: Session):
        self.session = session
        self.channel_api = ChannelApi(api_client=self.session.client)
        self.user_api = UserApi(api_client=self.session.client)
        
    def get_messages(self, channel_id: str, limit: int = 10):
        '''
            チャンネルIDからメッセージを取得する
        '''
        messages = self.channel_api.get_messages(channel_id=channel_id, limit=limit)
        #TODO embedとかの処理
        return [Message(username=self.user_api.get_user(msg.user_id).name, content=msg.content, created_at=msg.created_at) for msg in messages]
    
    def post_message(self, channel_id: str, content: str):
        '''
            チャンネルIDにメッセージを投稿する
        '''
        request = PostMessageRequest(content=content, embed=True)
        self.channel_api.post_message(channel_id=channel_id, post_message_request=request)