# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.user_stats import UserStats

class TestUserStats(unittest.TestCase):
    """UserStats unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UserStats:
        """Test UserStats
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UserStats`
        """
        model = UserStats()
        if include_optional:
            return UserStats(
                total_message_count = 56,
                stamps = [
                    openapi_client.models.user_stats_stamp.UserStatsStamp(
                        id = '', 
                        count = 56, 
                        total = 56, )
                    ],
                datetime_ = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return UserStats(
                total_message_count = 56,
                stamps = [
                    openapi_client.models.user_stats_stamp.UserStatsStamp(
                        id = '', 
                        count = 56, 
                        total = 56, )
                    ],
                datetime_ = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
        )
        """

    def testUserStats(self):
        """Test UserStats"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
