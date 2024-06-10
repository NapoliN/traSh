'''
    traq_shellをテストするモジュール
    sessionをテストするモジュール
'''
import os
from test.utils import getLoginId, getSession
from src.shell.session import Session

def test_try_login():
    '''
        loginのテスト
    '''
    usrname, password = getLoginId()
    session = Session()
    session.try_login(usrname, password)
    session_id = os.environ.get("QTRASH_SESSION")
    # セッションが記録できてるか
    assert session_id is not None

