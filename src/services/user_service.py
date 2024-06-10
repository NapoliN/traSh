from typing import List
from src.shell.session import Session
from openapi.openapi_client.api import UserApi

class UserService:
    #TODO Environmentを利用したキャッシュの有効化
    def __init__(self, session: Session):
        self.session = session
        self.user_api = UserApi(api_client=session.client)
        
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
    