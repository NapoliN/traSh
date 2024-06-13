'''
    chnotコマンド: チャンネルの通知設定を変更する 
'''
from typing import Optional
import argparse
import sys

from src.shell.session import Session
from src.shell.environment import Environment
from src.services.channel_service import ChannelService
from src.services.notification_service import NotificationService, NotificationState
from src.services.user_service import UserService

class InvalidNotifyValue(Exception):
    '''
        通知設定が不正な場合の例外
    '''

def chnot(path: str, notify: NotificationState, target: Optional[str]=None):
    """
        chnot: Change Notify
        0: 通知しない
        1: 未読通知
        2: 未読通知＋通知
        targetが自分でない場合、通知変更は0or2のみ
    """
    session = Session()
    session.load_session()
    env = Environment()
    channel_service = ChannelService(session)
    notification_service = NotificationService(session)
    user_service = UserService(session)
    _chnot(path, notify, env, channel_service, notification_service, user_service, target)

def _chnot(path: str, notify: NotificationState, env:Environment, channel_service:ChannelService, notification_service:NotificationService, user_service:UserService, target: Optional[str]=None):
    channel_id = channel_service.convert_path2idperfect(env.current_channel_id, path)
    if channel_id is None:
        print("チャンネルが見つかりませんでした")
        return
    fullpath = channel_service.convert_id2fullpath(channel_id)

    if target is None:
        # 自分の通知設定を変更
        notification_service.modify_my_subscription(channel_id, notify)
        print(f"{fullpath} の通知設定を '{ notify_value_str(notify) }' に変更しました。")
    else:
        # 他のユーザの通知設定を変更
        user_id = user_service.get_user_id(target)
        if notify == NotificationState.UNREAD_NOTIFY:
            print("他のユーザの通知設定の変更は0:通知しない 2:未読通知＋通知 のみ有効です")
            return
        notification_service.modify_subscribe(channel_id, user_id, notify == NotificationState.NOTIFY)
        print(f"{target} の {fullpath} の通知設定を '{ notify_value_str(notify) }' に変更しました。")

def get_notify_value(notify:str) -> NotificationState:
    if notify == "0":
        return NotificationState.NOT_NOTIFY
    elif notify == "1":
        return NotificationState.UNREAD_NOTIFY
    elif notify == "2":
        return NotificationState.NOTIFY
    else:
        raise InvalidNotifyValue("Invalid Notify Value: 0-unnotify, 1-unread notify, 2-notify.")

def notify_value_str(notify:NotificationState) -> str:
    if notify == NotificationState.NOT_NOTIFY:
        return "通知しない"
    elif notify == NotificationState.UNREAD_NOTIFY:
        return "未読通知"
    elif notify == NotificationState.NOTIFY:
        return "未読通知＋通知"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default=".")
    parser.add_argument("notify")
    parser.add_argument("-t", "--target")
    args = parser.parse_args()
    path = args.path
    try:
        notify = get_notify_value(args.notify)
    except InvalidNotifyValue as e:
        print(e)
        sys.exit(1)
    target = args.target
    chnot(path, notify, target)