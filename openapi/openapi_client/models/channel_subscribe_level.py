# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class ChannelSubscribeLevel(int, Enum):
    """
    チャンネル購読レベル 0：無し 1：未読管理 2：未読管理+通知
    """

    """
    allowed enum values
    """
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ChannelSubscribeLevel from a JSON string"""
        return cls(json.loads(json_str))


