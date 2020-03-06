import channels
import pytest
from error import InputError

def test_channels_create():
    assert channels.channels_create(12345, 'Ben', False) == 1
    assert channels.channels_create(12345, 'Bob', True) == 1
    list_of_channels = channels_listall(12345)
    
    #check if it has the names in it
    flag =0
    if Bob in list_of_channels[name]
        flag =1
    assert flag == 1


def test_channels_except():
    with pytest.raises(InputError) as e:
        channels.channels_create(12345,'yeeeeeeeeeeeeeeeeeeeeet',True)
