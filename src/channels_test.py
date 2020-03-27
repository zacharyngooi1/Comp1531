import pytest
from error import InputError, AccessError
from user import user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile
from other import users_all, search
from message import message_send
from channel import channels_create, channels_list_all
import datetime
from auth import auth_register
from db import token_check, email_check, email_dupe_check, get_messages_store, get_user_store, get_channel_store

# First create a dummy user
hamish_token = auth_register('haydenishere@gmail.com', 'this_ispass', 'hayden', 'smith')
hamish = token_check(hamish_token['token'])
zach_token = auth_register('Zacharyngooi@gmail.com', 'password', 'Zachary', 'Ngooi')
zach = token_check(zach_token['token'])
kelly_token = auth_register('kellywolfe@gmail.com', 'Password', 'Kelly', 'Wolfe')
kelly = token_check(kelly_token['token'])

def test_channels_create_invalid():
    with pytest.raises(InputError):
        channels_create(hamish['token'], 'BenBenBenBenBenBenBenBenBenBenBenBenBenBen', True)
   
def test_channels_create_valid():
    channel_id = channels_create(hamish_token['token'], 'New_channel', True)
    # Now to call our storage and assert that the channel_id is present in our store
    channel_store = get_channel_store()
    result = False
    for probe in channel_store['Channels']:
        if probe['channel_id'] == channel_id['channel_id']:
            result = True
    # Now we assert the value of result
    assert(result == True)
