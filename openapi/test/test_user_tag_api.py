# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.api.user_tag_api import UserTagApi


class TestUserTagApi(unittest.TestCase):
    """UserTagApi unit test stubs"""

    def setUp(self) -> None:
        self.api = UserTagApi()

    def tearDown(self) -> None:
        pass

    def test_add_my_user_tag(self) -> None:
        """Test case for add_my_user_tag

        自分にタグを追加
        """
        pass

    def test_add_user_tag(self) -> None:
        """Test case for add_user_tag

        ユーザーにタグを追加
        """
        pass

    def test_edit_my_user_tag(self) -> None:
        """Test case for edit_my_user_tag

        自分のタグを編集
        """
        pass

    def test_edit_user_tag(self) -> None:
        """Test case for edit_user_tag

        ユーザーのタグを編集
        """
        pass

    def test_get_my_user_tags(self) -> None:
        """Test case for get_my_user_tags

        自分のタグリストを取得
        """
        pass

    def test_get_tag(self) -> None:
        """Test case for get_tag

        タグ情報を取得
        """
        pass

    def test_get_user_tags(self) -> None:
        """Test case for get_user_tags

        ユーザーのタグリストを取得
        """
        pass

    def test_remove_my_user_tag(self) -> None:
        """Test case for remove_my_user_tag

        自分からタグを削除します
        """
        pass

    def test_remove_user_tag(self) -> None:
        """Test case for remove_user_tag

        ユーザーからタグを削除します
        """
        pass


if __name__ == '__main__':
    unittest.main()
