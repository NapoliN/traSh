from typing import Optional
from abc import ABCMeta, abstractmethod
import re
import certifi
import os
from dotenv import load_dotenv

from openapi.openapi_client import api_client
from openapi.openapi_client.models import PostLoginRequest
from openapi.openapi_client.api import AuthenticationApi, MeApi
from openapi.openapi_client.configuration import Configuration

class LoginFailException(Exception):
    '''
        ログインに失敗したときの例外
    '''

class SessionBase(metaclass=ABCMeta):
    @abstractmethod
    def load_session(self):
        pass
    @abstractmethod
    def try_login(self, username: str, password: str):
        pass
    @abstractmethod
    def try_exit(self):
        pass

class Session(SessionBase):
    '''
        sessionクラス
    '''
    def __init__(self):
        self.session_id = None
        # sessionを保持するためのクライアントを作成
        self.client = api_client.ApiClient(configuration=api_client.Configuration(ssl_ca_cert=certifi.where()))
        config = Configuration()
        load_dotenv(".env")
        
        config.host = os.getenv("TRAQ_API_ENDPOINT")
        self.client.configuration = config
        
    def load_session(self):
        '''
            環境変数からセッションを読み込む
        '''
        session_id = os.environ.get("QTRASH_SESSION")
        if session_id is None:
            raise Exception("No Session Found. Please set QTRASH_SESSION environment variable.")
        self.client.cookie = session_id
        
    # ログインを試行する
    def try_login(self, username: str, password: str):
        '''
            ログイン用
        '''
        auth_api = AuthenticationApi(api_client=self.client)
        try:
            res = auth_api.login_with_http_info(post_login_request=PostLoginRequest(name=username, password=password))
            if res.status_code != 204:
                raise LoginFailException("IDもしくはパスワードが違います。")
        except Exception as e:
            raise LoginFailException("apiに接続できませんでした。") from e
        assert res.headers is not None

        # cookieからセッションIDをもってきて設定する
        cookie = res.headers["Set-Cookie"]
        session = re.match(r"(r_session=.*?);", cookie)
        if session is None:
            raise Exception("セッションIDが取得できませんでした。")
        session_id = session.group(1)
        self.client.cookie = session_id
        os.environ.setdefault("QTRASH_SESSION", session_id)

    def try_exit(self):
        '''
            ログアウトを試行する
        '''
        auth_api = AuthenticationApi(api_client=self.client)
        res = auth_api.logout_with_http_info()
        if res.status_code != 204:
            raise Exception("ログアウトに失敗しました")
        print("ログアウトしました。")
        exit(0)