import pytest 
from channel import channel_join, channel_addowner, channel_removeowner, channel_details
from channel import channel_list, channels_list_all, channels_create, channel_leave, channel_invite
from auth import auth_register
from error import InputError, AccessError
from user import user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile
from other import users_all, search
import datetime
from auth import auth_register
from db import token_check, email_check, email_dupe_check, get_messages_store, channel_check, u_id_check, handle_check, get_channel_store

def test_auth_register_invalid():
	with pytest.raises(InputError):
		auth_register('email@hat', 'password','name_first', 'name_last')
	



