# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.api.stamp_api import StampApi


class TestStampApi(unittest.TestCase):
    """StampApi unit test stubs"""

    def setUp(self) -> None:
        self.api = StampApi()

    def tearDown(self) -> None:
        pass

    def test_add_message_stamp(self) -> None:
        """Test case for add_message_stamp

        スタンプを押す
        """
        pass

    def test_change_stamp_image(self) -> None:
        """Test case for change_stamp_image

        スタンプ画像を変更
        """
        pass

    def test_create_stamp(self) -> None:
        """Test case for create_stamp

        スタンプを作成
        """
        pass

    def test_create_stamp_palette(self) -> None:
        """Test case for create_stamp_palette

        スタンプパレットを作成
        """
        pass

    def test_delete_stamp(self) -> None:
        """Test case for delete_stamp

        スタンプを削除
        """
        pass

    def test_delete_stamp_palette(self) -> None:
        """Test case for delete_stamp_palette

        スタンプパレットを削除
        """
        pass

    def test_edit_stamp(self) -> None:
        """Test case for edit_stamp

        スタンプ情報を変更
        """
        pass

    def test_edit_stamp_palette(self) -> None:
        """Test case for edit_stamp_palette

        スタンプパレットを編集
        """
        pass

    def test_get_message_stamps(self) -> None:
        """Test case for get_message_stamps

        メッセージのスタンプリストを取得
        """
        pass

    def test_get_my_stamp_history(self) -> None:
        """Test case for get_my_stamp_history

        スタンプ履歴を取得
        """
        pass

    def test_get_stamp(self) -> None:
        """Test case for get_stamp

        スタンプ情報を取得
        """
        pass

    def test_get_stamp_image(self) -> None:
        """Test case for get_stamp_image

        スタンプ画像を取得
        """
        pass

    def test_get_stamp_palette(self) -> None:
        """Test case for get_stamp_palette

        スタンプパレットを取得
        """
        pass

    def test_get_stamp_palettes(self) -> None:
        """Test case for get_stamp_palettes

        スタンプパレットのリストを取得
        """
        pass

    def test_get_stamp_stats(self) -> None:
        """Test case for get_stamp_stats

        スタンプ統計情報を取得
        """
        pass

    def test_get_stamps(self) -> None:
        """Test case for get_stamps

        スタンプリストを取得
        """
        pass

    def test_remove_message_stamp(self) -> None:
        """Test case for remove_message_stamp

        スタンプを消す
        """
        pass


if __name__ == '__main__':
    unittest.main()
