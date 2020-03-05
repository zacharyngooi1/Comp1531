import message
import pytest
from error import InputError

def test_message_send():
    assert channels.message_send(12345, 12, 'hello hru') == 1

def test_message_except():
    with pytest.raises(InputError) as e:
        assert channels.message_send(12345, 12, 'a'*1001)
        #how do I check fro access errors??
