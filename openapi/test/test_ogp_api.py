# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.api.ogp_api import OgpApi


class TestOgpApi(unittest.TestCase):
    """OgpApi unit test stubs"""

    def setUp(self) -> None:
        self.api = OgpApi()

    def tearDown(self) -> None:
        pass

    def test_delete_ogp_cache(self) -> None:
        """Test case for delete_ogp_cache

        OGP情報のキャッシュを削除
        """
        pass

    def test_get_ogp(self) -> None:
        """Test case for get_ogp

        OGP情報を取得
        """
        pass


if __name__ == '__main__':
    unittest.main()
