# OIDCTraqUserInfo

traQ特有のユーザー詳細情報

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bio** | **str** | 自己紹介(biography) | 
**groups** | **List[str]** | 所属グループのUUIDの配列 | 
**tags** | [**List[UserTag]**](UserTag.md) | タグリスト | 
**last_online** | **datetime** | 最終オンライン日時 | 
**twitter_id** | **str** | Twitter ID | 
**display_name** | **str** | ユーザー表示名 | 
**icon_file_id** | **str** | アイコンファイルUUID | 
**bot** | **bool** | BOTかどうか | 
**state** | [**UserAccountState**](UserAccountState.md) |  | 
**permissions** | [**List[UserPermission]**](UserPermission.md) | 所有している権限の配列 | 
**home_channel** | **str** | ホームチャンネル | 

## Example

```python
from openapi_client.models.oidc_traq_user_info import OIDCTraqUserInfo

# TODO update the JSON string below
json = "{}"
# create an instance of OIDCTraqUserInfo from a JSON string
oidc_traq_user_info_instance = OIDCTraqUserInfo.from_json(json)
# print the JSON string representation of the object
print(OIDCTraqUserInfo.to_json())

# convert the object into a dict
oidc_traq_user_info_dict = oidc_traq_user_info_instance.to_dict()
# create an instance of OIDCTraqUserInfo from a dict
oidc_traq_user_info_form_dict = oidc_traq_user_info.from_dict(oidc_traq_user_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


