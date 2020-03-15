import channels
import pytest
from error import InputError

def test_channels_create():
    channels.channels_create(12345, 'Ben', False) = ch_id
    list_of_channels = channels_listall(12345)
    #check if it has the names in it
    flag =0
        
    if ch_id in list_of_channels['channel_id']:
        flag =1
    assert flag == 1

def test_channels_except():
    with pytest.raises(InputError) as e:
        channels.channels_create(12345,'yeeeeeeeeeeeeeeeeeeeeet',True)#channel name linger than 20 characters
