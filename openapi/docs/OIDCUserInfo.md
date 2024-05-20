# OIDCUserInfo

自分のユーザー詳細情報

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub** | **str** | ユーザーUUID | 
**name** | **str** | ユーザー名 | 
**preferred_username** | **str** | ユーザー名 | 
**picture** | **str** | アイコン画像URL | 
**updated_at** | **int** | 更新日時 | [optional] 
**traq** | [**OIDCTraqUserInfo**](OIDCTraqUserInfo.md) |  | [optional] 

## Example

```python
from openapi_client.models.oidc_user_info import OIDCUserInfo

# TODO update the JSON string below
json = "{}"
# create an instance of OIDCUserInfo from a JSON string
oidc_user_info_instance = OIDCUserInfo.from_json(json)
# print the JSON string representation of the object
print(OIDCUserInfo.to_json())

# convert the object into a dict
oidc_user_info_dict = oidc_user_info_instance.to_dict()
# create an instance of OIDCUserInfo from a dict
oidc_user_info_form_dict = oidc_user_info.from_dict(oidc_user_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


