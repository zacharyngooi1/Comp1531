import channels
import pytest
from error import InputError

def test_channel_create():
    assert channels.channels_create(12345, 'Bob', True) == 1
    assert channels.channels_create(12345, 'Bob', False) == 1
    assert channels.channels_create(12345, '', False) == 0
    assert channels.channels_create(, 'Bob', False) == 0
    assert channels.channels_create(, '', False) == 0
    assert channels.channels_create(, '', ) == 0

def test_channel_except():
    with pytest.raises(InputError) as e:
        #assert channels.channels_create() HOW DO I TEST THE INPUT VARIABLE??
        assert channels.channels_create(12345,'yeeeeeeeeeeeeeeeeeeeeet',True)
