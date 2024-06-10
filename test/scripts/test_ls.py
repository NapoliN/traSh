from typing import List
import pytest
from src.scripts.ls import _ls
from test.mock.channel_service_mock import ChannelSeerviceMock
from test.mock.environment_mock import EnvironmentMock

def test_ls_current(capfd: pytest.CaptureFixture):
    channel_service = ChannelSeerviceMock()
    env = EnvironmentMock()
    _ls(".", channel_service, env)
    res = capfd.readouterr()
    out: str = res.out
    out_list = out.split("\n")
    assert out_list[0] == "root_channel_name"
    assert out_list[1] == "--channel1_name"
    assert out_list[2] == "--channel2_name"
    
def test_ls_recursive(capfd: pytest.CaptureFixture):
    channel_service = ChannelSeerviceMock()
    env = EnvironmentMock()
    _ls(".", channel_service, env, recursive=True)
    res = capfd.readouterr()
    out: str = res.out
    out_list = out.split("\n")
    assert out_list[0] == "root_channel_name"
    assert out_list[1] == "--channel1_name"
    assert out_list[2] == "----channel1_1_name"
    assert out_list[3] == "--channel2_name"