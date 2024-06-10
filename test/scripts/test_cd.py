import os
from test.mock.channel_service_mock import ChannelSeerviceMock
from test.mock.environment_mock import EnvironmentMock
from src.scripts.cd import _cd


def test_cd():
    channel_service = ChannelSeerviceMock()
    env = EnvironmentMock()
    _cd("channel1_name/channel1_1_name", channel_service, env)
    assert env.current_channel_id == "channel1_1"