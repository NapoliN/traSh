from typing import List, Optional
from openapi.openapi_client.models import ChannelList, Channel
from src.shell.environment import IEnvironment

class EnvironmentMock(IEnvironment):
    def __init__(self):
        self.__current_channel_id = "root_channel"
        self.__current_channel_name = "root_channel_name"
        
    def set_current_channel(self, channel_id: str, channel_name: str):
        self.__current_channel_id = channel_id
        self.__current_channel_name = channel_name
    
    @property
    def current_channel_id(self):
        return self.__current_channel_id
    
    @property
    def current_channel_name(self):
        return self.__current_channel_name
    
    def set_channels(self, channels: ChannelList):
        return
    
    def get_channel_ids(self) -> Optional[List[str]]:
        return ["root_channel", "channel1", "channel2", "channel1_1"]
    
    def get_channel(self, channel_id: str) -> Channel:
        if channel_id == "root_channel":
            return Channel(id="root_channel", name="root_channel_name", parentId=None, archived=False, force=False, topic="channel1_topic", children=["channel1", "channel2"])
        elif channel_id == "channel1":
            return Channel(id="channel1", name="channel1_name", parentId="root_channel", archived=False, force=False, topic="channel1_topic", children=["channel1_1"])
        elif channel_id == "channel2":
            return Channel(id="channel2", name="channel2_name", parentId="root_channel", archived=False, force=False, topic="channel2_topic", children=[])
        elif channel_id == "channel1_1":
            return Channel(id="channel1_1", name="channel1_1_name", parentId="channel1", archived=False, force=False, topic="channel1_1_topic", children=[])
        raise Exception("Channel Not Found")