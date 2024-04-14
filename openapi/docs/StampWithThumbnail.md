# StampWithThumbnail

スタンプ情報とサムネイルの有無

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | スタンプUUID | 
**name** | **str** | スタンプ名 | 
**creator_id** | **str** | 作成者UUID | 
**created_at** | **datetime** | 作成日時 | 
**updated_at** | **datetime** | 更新日時 | 
**file_id** | **str** | ファイルUUID | 
**is_unicode** | **bool** | Unicode絵文字か | 
**has_thumbnail** | **bool** | サムネイルの有無 | 

## Example

```python
from openapi_client.models.stamp_with_thumbnail import StampWithThumbnail

# TODO update the JSON string below
json = "{}"
# create an instance of StampWithThumbnail from a JSON string
stamp_with_thumbnail_instance = StampWithThumbnail.from_json(json)
# print the JSON string representation of the object
print(StampWithThumbnail.to_json())

# convert the object into a dict
stamp_with_thumbnail_dict = stamp_with_thumbnail_instance.to_dict()
# create an instance of StampWithThumbnail from a dict
stamp_with_thumbnail_form_dict = stamp_with_thumbnail.from_dict(stamp_with_thumbnail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


