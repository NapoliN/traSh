# coding: utf-8

"""
    traQ v3

    traQ v3 API

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List
from openapi_client.models.user_stats_stamp import UserStatsStamp
from typing import Optional, Set
from typing_extensions import Self

class UserStats(BaseModel):
    """
    ユーザー統計情報
    """ # noqa: E501
    total_message_count: StrictInt = Field(description="ユーザーの総投稿メッセージ数(削除されたものも含む)", alias="totalMessageCount")
    stamps: List[UserStatsStamp] = Field(description="ユーザーのスタンプ統計情報")
    datetime_: datetime = Field(description="統計情報日時")
    __properties: ClassVar[List[str]] = ["totalMessageCount", "stamps", "datetime_"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UserStats from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in stamps (list)
        _items = []
        if self.stamps:
            for _item in self.stamps:
                if _item:
                    _items.append(_item.to_dict())
            _dict['stamps'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserStats from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "totalMessageCount": obj.get("totalMessageCount"),
            "stamps": [UserStatsStamp.from_dict(_item) for _item in obj["stamps"]] if obj.get("stamps") is not None else None,
            "datetime_": obj.get("datetime_")
        })
        return _obj


