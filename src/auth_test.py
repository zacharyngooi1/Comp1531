import pytest 
from channel import channel_join, channel_addowner, channel_removeowner, channel_details
from channel import channel_list, channels_list_all, channels_create, channel_leave, channel_invite
from auth import auth_register
from error import InputError, AccessError
from user import user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile
from other import users_all, search
import datetime
from auth import auth_register, auth_login, auth_logout
from db import token_check, email_check, email_dupe_check, get_messages_store, channel_check, u_id_check, handle_check, get_channel_store, get_user_store

def test_auth_register_invalid():
	with pytest.raises(InputError):
		auth_register('email@hat', 'password','name_first', 'name_last')
		auth_register('kellywolfe@gmail.com', 'Password1233', 'gigit', 'apple')
		auth_register('emaihrhfl@hotmail.com', 'six','name_first', 'name_last')
		auth_register('emaihrhfl@hotmail.com', 'sixting','', 'name_last')
		auth_register('emaihrhfl@hotmail.com', 'sixting','name_firstname_firstname_firstname_firstname_firstname_firstname_firstname_firstname_firstname_firstname_firstname_firstname_firstname_firstname_first', 'name_last')
		auth_register('emaihrhfl@hotmail.com', 'sixtingpass','name_first', '')
		auth_register('emaihrhfl@hotmail.com', 'sixtingpass','name_first', 'name_lastname_lastname_lastname_lastname_lastname_lastname_lastname_lastname_lastname_lastname_lastname_lastname_lastname_lastname_last')

def test_auth_register_valid():
	kelly_token = auth_register('kellywolfe@gmail.com', 'Password', 'Kelly', 'Wolfe')
	kelly = token_check(kelly_token['token'])
	assert(kelly_token == {
		'u_id': kelly['u_id'],
		'token': kelly['token']
	})

	# Test for creation of unique handle
	zach_token = auth_register('Zacharyngooi@gmail.com', 'password', 'Kelly', 'Wolfe')
	zach = token_check(zach_token['token'])
	assert(zach['handle_str'] != kelly['handle_str'])

def test_auth_register_valid_length_handle():
	user_token = auth_register('haydenishere@gmail.com', 'this_ispass', 'abcdefghijihbfruhbfhr', 'ewgvfhvwrhfbjhrwfbjrjhfbwjrnfkrw')
	hamish = token_check(user_token['token'])
	assert(len(hamish['handle_str']) <= 20)

def test_auth_login_invalid():
	with pytest.raises(InputError):
		auth_login("hot@ems", 'password')
		auth_login('helloitsme@hotmail.com','password')
		auth_login('haydenishere@gmail.com', 'Wrongpass')


def test_auth_logout_invalid():
	assert(auth_logout('This_is_a_wrong_token') == False)

# Create a dummy user
dummy_token = auth_register('dummy@gmail.com', 'worthwile', 'dummyt', 'loopy')
dummy = token_check(dummy_token['token'])

def test_auth_logout_valid():
	# Log dummy out
	assert(auth_logout(dummy['token']) == True)

def test_auth_login_valid():
	result = False
	# Now we log him in
	token_holder = auth_login('dummy@gmail.com','worthwile')
	storage = get_user_store()
	for users in storage['users']:
		print(users)
		if users['token'] == token_holder['token']:
			result = True

	assert(result == True)

