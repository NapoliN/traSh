from typing import List, Optional
from src.services.channel_service import IChannelService

class ChannelSeerviceMock(IChannelService):
    def __init__(self):
        pass

    def get_channel_name(self, channel_id:str) -> str:
        if channel_id == "root_channel":
            return "root_channel_name"
        elif channel_id == "channel1":
            return "channel1_name"
        elif channel_id == "channel2":
            return "channel2_name"
        elif channel_id == "channel1_1":
            return "channel1_1_name"
        else:
            raise Exception("Channel Not Found")
    
    def convert_id2fullpath(self, channel_id:str) -> str:
        if channel_id == "root_channel":
            return "#root_channel_name"
        elif channel_id == "channel1":
            return "#root_channel_name/channel1_name"
        elif channel_id == "channel2":
            return "#root_channel_name/channel2_name"
        elif channel_id == "channel1_1":
            return "#root_channel_name/channel1_name/channel1_1_name"
        else:
            raise Exception("Channel Not Found")
    
    def convert_path2idprefix(self, current_channel_id: str, path_:str) -> List[str]:
        if current_channel_id == "root_channel" and path_ == "channel1_name/channel":
            return ["channel1_1"]
        raise NotImplementedError("Not Implemented")
    
    def convert_path2idperfect(self, current_channel_id: str, path_:str) -> Optional[str]:
        if current_channel_id == "root_channel" and path_ == ".":
            return "root_channel"
        elif current_channel_id == "root_channel" and path_ == "channel1_name/channel1_1_name":
            return "channel1_1"
        else:
            raise NotImplementedError("Not Implemented")
    
    def print_channel_tree(self, channel_id: str, recursive: bool = False, archived: bool = False):
        if channel_id == "root_channel":
            if recursive:
                print("root_channel_name")
                print("--channel1_name")
                print("----channel1_1_name")
                print("--channel2_name")
            else:
                print("root_channel_name")
                print("--channel1_name")
                print("--channel2_name")
        elif channel_id == "channel1":
                print("channel1_name")
                print("--channel1_1_name")
        elif channel_id == "channel2":
            print("channel2_name")