# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.patch_me_request import PatchMeRequest

class TestPatchMeRequest(unittest.TestCase):
    """PatchMeRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PatchMeRequest:
        """Test PatchMeRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PatchMeRequest`
        """
        model = PatchMeRequest()
        if include_optional:
            return PatchMeRequest(
                display_name = '',
                twitter_id = 'HqXzyC',
                bio = '',
                home_channel = ''
            )
        else:
            return PatchMeRequest(
        )
        """

    def testPatchMeRequest(self):
        """Test PatchMeRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
