from src.services import ChannelService
from src.shell.session import Session
    
from test.mock.channel_api_mock import ChannelApiMock

vacant_session = Session()
channel_service = ChannelService(session=vacant_session)
channel_service.channel_api = ChannelApiMock() # type: ignore

def test_get_channel_name():
    root_channel_name = channel_service.get_channel_name("root_channel")
    assert root_channel_name == "root_channel_name"
    
def test_convert_id2name():
    channel1_name = channel_service.convert_id2fullpath("channel1")
    assert channel1_name == "#root_channel_name/channel1_name"
    
def test_convert_path2idprefix():
    channel1_1_id = channel_service.convert_path2idprefix("root_channel", "channel1_name/channel")
    assert channel1_1_id == ["channel1_1"]
    
def test_convert_path2idprefix_multiple():
    candidates = channel_service.convert_path2idprefix("root_channel", "./channel")
    assert candidates == ["channel1", "channel2"]
    
def test_convert_path2idprefix_root():
    root_id = channel_service.convert_path2idprefix("channel1", "#root_channel_")
    assert root_id == ["root_channel"]

def test_convert_path2idprefix_absolute():
    channel1_1_id = channel_service.convert_path2idprefix("root_channel", "#root_channel_name/channel")
    assert channel1_1_id == ["channel1", "channel2"]
    
def test_convert_path2idperfect():
    channel1_1_id = channel_service.convert_path2idperfect("root_channel", "channel1_name/channel1_1_name")
    assert channel1_1_id == "channel1_1"

def test_convert_path2idperfect_relative():
    channel2_id = channel_service.convert_path2idperfect("root_channel", "./channel2_name")
    assert channel2_id == "channel2"
    
def test_convert_path2idperfect_parent():
    root_id = channel_service.convert_path2idperfect("channel1", "..")
    assert root_id == "root_channel"

def test_convert_path2idperfect_root():
    root_id = channel_service.convert_path2idperfect("channel1", "#root_channel_name")
    assert root_id == "root_channel"

def test_convert_path2idperfect_absolute():
    channel1_1_id = channel_service.convert_path2idperfect("root_channel", "#root_channel_name/channel1_name/channel1_1_name")
    assert channel1_1_id == "channel1_1"