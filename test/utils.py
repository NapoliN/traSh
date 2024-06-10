import os
from typing import Tuple
from src.shell.session import Session


def getLoginId() -> Tuple[str,str]:
    usrname = os.environ.get("TRAQ_USERNAME")
    password = os.environ.get("TRAQ_PASSWORD")
    if usrname is None or password is None:
        raise Exception("Please set TRAQ_USERNAME and TRAQ_PASSWORD environment variables.")
    return usrname, password

def getSession() -> Session:
    '''
        ログイン済みsessionを取得する
    '''
    usrname, password = getLoginId()
    session = Session()
    session.try_login(usrname, password)
    return session