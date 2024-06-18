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

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from openapi_client.models.user_account_state import UserAccountState
from typing import Optional, Set
from typing_extensions import Self

class PatchUserRequest(BaseModel):
    """
    ユーザー情報編集リクエスト
    """ # noqa: E501
    display_name: Optional[Annotated[str, Field(strict=True, max_length=32)]] = Field(default=None, description="新しい表示名", alias="displayName")
    twitter_id: Optional[Annotated[str, Field(strict=True)]] = Field(default=None, description="TwitterID", alias="twitterId")
    state: Optional[UserAccountState] = None
    role: Optional[StrictStr] = Field(default=None, description="ユーザーロール")
    __properties: ClassVar[List[str]] = ["displayName", "twitterId", "state", "role"]

    @field_validator('twitter_id')
    def twitter_id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9_]{0,15}$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9_]{0,15}$/")
        return value

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
        """Create an instance of PatchUserRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchUserRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "displayName": obj.get("displayName"),
            "twitterId": obj.get("twitterId"),
            "state": obj.get("state"),
            "role": obj.get("role")
        })
        return _obj


