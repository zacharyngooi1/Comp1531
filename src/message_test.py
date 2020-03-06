import message
import channels
import pytest
from error import InputError

def test_message_send():
    assert message.message_send(12345, 1, 'hello hru') == 1
    
    
def test_message_send():
    assert message_remove(12345,1) == {}

def test_message_send():
    assert message_remove(12345,1) == {}

def test_message_except():
    with pytest.raises(InputError) as e:
        assert message.message_send(12345, 1, 'a'*1001)
        #how do I check fro access errors??

    list_of_channels = channels_listall(12345)
    flag =1
    if Bob in list_of_channels[name]:
        flag = 0
    with pytest.raises(AccessError) as e:
        assert flag == 1
