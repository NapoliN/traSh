'''
    traq_shellをテストするモジュール
    sessionをテストするモジュール
'''
import os
from src.shell.traq_shell import TraQShell
from src.shell.session import Session
from src.shell.environment import Environment

USERNAME = os.environ.get("TRAQ_USERNAME")
PASSWORD = os.environ.get("TRAQ_PASSWORD")
if USERNAME is None or PASSWORD is None:
    raise Exception("Please set TRAQ_USERNAME and TRAQ_PASSWORD environment variables.")

def test_session():
    '''
        sessionのテスト
    '''
    session = Session()
    session.try_login(USERNAME, PASSWORD)
    session_id = os.environ.get("QTRASH_SESSION")
    assert session_id is not None