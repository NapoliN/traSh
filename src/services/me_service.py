'''
    自分のアカウントの情報を取得/変更するサービス
'''
from src.shell.session import Session
from openapi_client.api.me_api import MeApi


class MeService:
    def __init__(self, session:Session) -> None:
        self.me_api = MeApi(api_client=session.client)
        