import user
import pytest
from error import InputError

def test_user_profile():
    assert user.user_profile(12345, 1) ==  {'u_id': 1,'email': 'cs1531@cse.unsw.edu.au','name_first': 'Hayden','name_last': 'Jacobs', 	'handle_str': 'hjacobs'}
   
def test_user_profile():
    with pytest.raises(InputError) as e:
        #assert channels.channels_create() HOW DO I TEST THE INPUT VARIABLE??
        assert user.user_profile(12345, 2) #technically u_id can be anything but 1
