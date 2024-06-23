'''passwd:  パスワードを変更します'''
import sys
from getpass import getpass

from src.services.user_service import UserService
from src.shell.session import Session

def passwd():
    session = Session()
    session.load_session()
    user_service = UserService(session)
    _passwd(user_service)


def _passwd(user_service:UserService):
    sys.stderr.write("パスワードを変更します。\n現在のパスワード: ")
    current_password = getpass()
    sys.stderr.write("新しいパスワード: ")
    new_password = getpass()
    try:
        user_service.change_password(current_password, new_password)
    except Exception as e:
        sys.stderr.write("パスワードの変更に失敗しました。\n")
        return
    sys.stderr.write("パスワードを変更しました。\n")
    
if __name__ == "__main__":
    passwd()