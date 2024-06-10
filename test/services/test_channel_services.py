from typing import List
from src.services import ChannelService
from src.shell.session import Session
from openapi.openapi_client.api import ChannelApi
from openapi.openapi_client.models import Channel, ChannelList

class ChannelApiMock():
    def __init__(self):
        self.channels = [
            Channel(id="root_channel", name="root_channel_name", parentId=None, archived=False, force=False, topic="channel1_topic", 
                    children=["channel1",
                              "channel2"
                              ]),
            Channel(id="channel1", name="channel1_name", parentId="root_channel", archived=False, force=False, topic="channel1_topic", children=["channel1_1"]),
            Channel(id="channel2", name="channel2_name", parentId="root_channel", archived=False, force=False, topic="channel2_topic", children=[]),
            Channel(id="channel1_1", name="channel1_1_name", parentId="channel1", archived=False, force=False, topic="channel1_1_topic", children=[]),
        ]
        
    def get_channel(self, channel_id) -> Channel:
        for chnl in self.channels:
            if chnl.id == channel_id:
                return chnl
        raise Exception("Channel Not Found")
    
    def get_channels(self) -> ChannelList:
        return ChannelList(public=self.channels)
    
vacant_session = Session()
channel_service = ChannelService(session=vacant_session)
channel_service.channel_api = ChannelApiMock() # type: ignore

def test_get_channel_name():
    root_channel_name = channel_service.get_channel_name("root_channel")
    assert root_channel_name == "root_channel_name"
    
def test_convert_id2name():
    channel1_name = channel_service.convert_id2name("channel1")
    assert channel1_name == "#root_channel_name/channel1_name"
    
def test_convert_name2idprefix():
    channel1_1_id = channel_service.convert_name2idprefix("root_channel", "channel1_name/channel")
    assert channel1_1_id == ["channel1_1"]
    
def test_convert_name2idperfect():
    channel1_1_id = channel_service.convert_name2idperfect("root_channel", "channel1_name/channel1_1_name")
    assert channel1_1_id == "channel1_1"