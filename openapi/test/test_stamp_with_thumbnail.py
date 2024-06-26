# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.stamp_with_thumbnail import StampWithThumbnail

class TestStampWithThumbnail(unittest.TestCase):
    """StampWithThumbnail unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> StampWithThumbnail:
        """Test StampWithThumbnail
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `StampWithThumbnail`
        """
        model = StampWithThumbnail()
        if include_optional:
            return StampWithThumbnail(
                id = '',
                name = 'zBAMDTMv2D2ylmgd10Z3UB6U',
                creator_id = '',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                file_id = '',
                is_unicode = True,
                has_thumbnail = True
            )
        else:
            return StampWithThumbnail(
                id = '',
                name = 'zBAMDTMv2D2ylmgd10Z3UB6U',
                creator_id = '',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                file_id = '',
                is_unicode = True,
                has_thumbnail = True,
        )
        """

    def testStampWithThumbnail(self):
        """Test StampWithThumbnail"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
