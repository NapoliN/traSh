'''
    ユーザ情報を取得/変更するサービス
'''
from typing import List
from src.shell.session import Session
from openapi.openapi_client.api import UserApi, MeApi
from openapi_client.models.put_my_password_request import PutMyPasswordRequest
from openapi_client.models.patch_me_request import PatchMeRequest

class UserService:
    '''
        ユーザ情報を取得/変更するサービスクラス
    '''
    #TODO Environmentを利用したキャッシュの有効化
    def __init__(self, session: Session):
        self.session = session
        self.user_api = UserApi(api_client=session.client)
        self.me_api = MeApi(api_client=session.client)

    def get_user_name(self, user_id:str) -> str:
        '''
            ユーザIDからユーザ名を取得する
            
            Args:
                user_id: ユーザID
        '''
        user = self.user_api.get_user(user_id=user_id)
        return user.name

    def get_user_names(self, user_ids:List[str]) -> List[str]:
        '''
            ユーザIDの配列をユーザ名の配列に変換する
        '''
        #TODO 愚直実装を直す
        user_names = []
        for user_id in user_ids:
            user_names.append(self.get_user_name(user_id))
        return user_names

    def get_user_id(self, user_name:str) -> str:
        '''
            ユーザ名からユーザIDを取得する
            
            Args:
                user_name: ユーザ名
        '''
        user = self.user_api.get_users(name=user_name)
        return user[0].id

    def change_password(self, current_password: str, new_password: str):
        '''
            パスワード変更
        '''
        request = PutMyPasswordRequest(password=current_password, newPassword=new_password)
        self.me_api.change_my_password(request)
        
    def change_displayname(self, new_displayname: str):
        '''
            表示名変更
        '''
        request = PatchMeRequest(displayName=new_displayname)
        self.me_api.edit_me(request)

    def change_home_channel(self, new_channel_id: str):
        '''
            ホームディレクトリ変更
        '''
        request = PatchMeRequest(homeChannel=new_channel_id)
        self.me_api.edit_me(request)