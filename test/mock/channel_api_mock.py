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

    def get_channel(self, channel_id:str) -> Channel:
        for chnl in self.channels:
            if chnl.id == channel_id:
                return chnl
        raise Exception("Channel Not Found")
    
    def get_channels(self) -> ChannelList:
        return ChannelList(public=self.channels)