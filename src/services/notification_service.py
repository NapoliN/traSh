import enum
from typing import List
from src.shell.session import Session
from src.shell.environment import Environment
from openapi.openapi_client.api import NotificationApi, MeApi
from openapi.openapi_client.models import PutChannelSubscribeLevelRequest, ChannelSubscribeLevel, PatchChannelSubscribersRequest

class NotificationState(enum.Enum):
    NOT_NOTIFY = 0
    UNREAD_NOTIFY = 1
    NOTIFY = 2

class NotificationService:
    '''
        通知編集周りのサービスクラス
    '''
    
    def __init__(self, session: Session):
        self.session = session
        self.env = Environment()
        self.notification_api = NotificationApi(api_client=self.session.client)
        self.me_api = MeApi(api_client=self.session.client)
        
    def get_subscriber(self, channel_id:str) -> List[str]:
        '''
            チャンネルの購読者のIDを取得する
        '''
        subscribers = self.notification_api.get_channel_subscribers(channel_id=channel_id)
        return subscribers
    
    def modify_subscribe(self, channel_id: str, user_id: str, is_subscribe: bool):
        '''
            ユーザのチャンネルの未読状態を変更する
        '''
        if is_subscribe:
            request = PatchChannelSubscribersRequest(on=[user_id])
        else:
            request = PatchChannelSubscribersRequest(off=[user_id])
        self.notification_api.edit_channel_subscribers(channel_id=channel_id, patch_channel_subscribers_request=request)
        
    def modify_my_subscription(self, channel_id, notify: NotificationState):
        '''
            自分の購読状態を変更する
        '''
        request = PutChannelSubscribeLevelRequest(level=ChannelSubscribeLevel(notify.value))
        self.me_api.set_channel_subscribe_level(channel_id=channel_id, put_channel_subscribe_level_request=request)