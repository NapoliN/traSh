# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.api.user_api import UserApi


class TestUserApi(unittest.TestCase):
    """UserApi unit test stubs"""

    def setUp(self) -> None:
        self.api = UserApi()

    def tearDown(self) -> None:
        pass

    def test_add_user_tag(self) -> None:
        """Test case for add_user_tag

        ユーザーにタグを追加
        """
        pass

    def test_change_user_icon(self) -> None:
        """Test case for change_user_icon

        ユーザーのアイコン画像を変更します
        """
        pass

    def test_change_user_password(self) -> None:
        """Test case for change_user_password

        ユーザーのパスワードを変更
        """
        pass

    def test_create_user(self) -> None:
        """Test case for create_user

        ユーザーを登録
        """
        pass

    def test_edit_user(self) -> None:
        """Test case for edit_user

        ユーザー情報を変更
        """
        pass

    def test_edit_user_tag(self) -> None:
        """Test case for edit_user_tag

        ユーザーのタグを編集
        """
        pass

    def test_get_direct_messages(self) -> None:
        """Test case for get_direct_messages

        ダイレクトメッセージのリストを取得
        """
        pass

    def test_get_user(self) -> None:
        """Test case for get_user

        ユーザー詳細情報を取得
        """
        pass

    def test_get_user_dm_channel(self) -> None:
        """Test case for get_user_dm_channel

        DMチャンネル情報を取得
        """
        pass

    def test_get_user_icon(self) -> None:
        """Test case for get_user_icon

        ユーザーのアイコン画像を取得
        """
        pass

    def test_get_user_stats(self) -> None:
        """Test case for get_user_stats

        ユーザー統計情報を取得
        """
        pass

    def test_get_user_tags(self) -> None:
        """Test case for get_user_tags

        ユーザーのタグリストを取得
        """
        pass

    def test_get_users(self) -> None:
        """Test case for get_users

        ユーザーのリストを取得
        """
        pass

    def test_post_direct_message(self) -> None:
        """Test case for post_direct_message

        ダイレクトメッセージを送信
        """
        pass

    def test_remove_user_tag(self) -> None:
        """Test case for remove_user_tag

        ユーザーからタグを削除します
        """
        pass


if __name__ == '__main__':
    unittest.main()
