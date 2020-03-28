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

# First create a dummy user
hamish_token = auth_register('haydenishere@gmail.com', 'this_ispass', 'hayden', 'smith')
hamish = token_check(hamish_token['token'])
zach_token = auth_register('Zacharyngooi@gmail.com', 'password', 'Zachary', 'Ngooi')
zach = token_check(zach_token['token'])
kelly_token = auth_register('kellywolfe@gmail.com', 'Password', 'Kelly', 'Wolfe')
kelly = token_check(kelly_token['token'])

# Now we create 3 channels and use them to test


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
	for probe in channel_store['Channels']:
		if probe['channel_id'] == channel_id['channel_id']:
			channel_store['Channels'].remove(probe)

# Lets go to our next tests
channel_id_hamish = channels_create(hamish_token['token'], 'Hamish_channel', True)
# Zachs channel will be private
channel_id_zach = channels_create(zach_token['token'], 'Zach_channel', False)

channel_id_kelly = channels_create(kelly_token['token'], 'Kelly_channel', True)

# As of now, each uer is a owner and a member of their channel

# Test invalid channel
def test_channel_details_invalid(): 
	with pytest.raises(AccessError):
		channel_details(zach['token'], channel_id_hamish['channel_id'])
	with pytest.raises(InputError):
		channel_details(zach['token'], 12345)

#returns basic information about a channel, including owner and member list 
def test_channel_details_valid():
	assert(channel_details(zach['token'], channel_id_zach['channel_id']) ==
	{
		'name': 'Zach_channel',

		'owner_members': [{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']}],

		'all_members':  [{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']}],

	} 
	)

#Tests that you cannot join a channel with an invalid ID or a private channel
def test_channel_join_id_invalid(): 
	with pytest.raises(InputError):
		channel_join(kelly['token'], 288374)
	# Since zachs channel is private, kelly can't join, Nice try Kelly
	with pytest.raises(AccessError):
		channel_join(kelly['token'], channel_id_zach['channel_id'])


#Tests to make sure a user can correctly join a channel 
def test_channel_join_correct(): 
	# Now lets have zach join kellys channel and assert that.
	assert(channel_details(kelly['token'], channel_id_kelly['channel_id']) ==
	{
		'name': 'Kelly_channel',

		'owner_members': [{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']}],

		'all_members':  [{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']}],

	} 
	)
	channel_join(zach['token'], channel_id_kelly['channel_id'])
	# Now we assert that zach is now a member in kelly's channel.
	assert(channel_details(kelly['token'], channel_id_kelly['channel_id']) ==
	{
		'name': 'Kelly_channel',

		'owner_members': [{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']}],

		'all_members':  [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']}
		],

	} 
	)

	#You know what lets have hamish join kellys channel too
	channel_join(hamish['token'], channel_id_kelly['channel_id'])
	assert(channel_details(kelly['token'], channel_id_kelly['channel_id']) ==
	{
		'name': 'Kelly_channel',

		'owner_members': [{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']}],

		'all_members':  [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']},

		{'name_first': hamish['name_first'], 
		'name_last': hamish['name_last'], 'u_id': hamish['u_id']}
		],
	}
	)

# Now we need to remmeber that kelly has 3 people in her channel for members
#Tests that you cannot add an owner to a channel with an invalid ID
def test_channel_addowner_id_invalid(): 
	with pytest.raises(InputError):
		#Lets test for wrong channel id first
		channel_addowner(kelly['token'], 63534, zach['u_id'])
		#Now test for alrady owner
		channel_addowner(kelly['token'], channel_id_kelly['channel_id'], kelly['u_id'])
	with pytest.raises(AccessError):
		channel_addowner(zach['token'], channel_id_kelly['channel_id'], hamish['u_id'])

#This checks if the owner has actually been added

def test_channel_addowner_added ():
	assert(channel_details(kelly['token'], channel_id_kelly['channel_id']) ==
	{
		'name': 'Kelly_channel',

		'owner_members': [{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']}],

		'all_members':  [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']},

		{'name_first': hamish['name_first'], 
		'name_last': hamish['name_last'], 'u_id': hamish['u_id']}
		],
	}
	)
	# Add zach as owner
	channel_addowner(kelly['token'], channel_id_kelly['channel_id'], zach['u_id'])
	assert(channel_details(kelly['token'], channel_id_kelly['channel_id']) ==
	{
		'name': 'Kelly_channel',

		'owner_members': [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']},

		],

		'all_members':  [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']},

		{'name_first': hamish['name_first'], 
		'name_last': hamish['name_last'], 'u_id': hamish['u_id']}
		],
	}
	)

def test_channel_remove_owner_invalid():
	with pytest.raises(InputError):
		#Lets test for wrong channel id first
		channel_removeowner(kelly['token'], 63534, zach['u_id'])
		#Now test for when not an owner
		channel_removeowner(kelly['token'], channel_id_kelly['channel_id'], hamish['u_id'])
	with pytest.raises(AccessError):
		# Only hamish is not an owner
		channel_removeowner(hamish['token'], channel_id_kelly['channel_id'], zach['u_id'])

def test_channel_remove_owner_valid():
	assert(channel_details(kelly['token'], channel_id_kelly['channel_id']) ==
	{
		'name': 'Kelly_channel',

		'owner_members': [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']},

		],

		'all_members':  [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']},

		{'name_first': hamish['name_first'], 
		'name_last': hamish['name_last'], 'u_id': hamish['u_id']}
		],
	}
	)

	# Now we remove owner zach
	channel_removeowner(kelly['token'], channel_id_kelly['channel_id'], zach['u_id'])
	assert(channel_details(kelly['token'], channel_id_kelly['channel_id']) ==
	{
		'name': 'Kelly_channel',

		'owner_members': [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},

		],

		'all_members':  [
			{'name_first': kelly['name_first'], 
		'name_last': kelly['name_last'], 'u_id': kelly['u_id']},
		
		{'name_first': zach['name_first'], 
		'name_last': zach['name_last'], 'u_id': zach['u_id']},

		{'name_first': hamish['name_first'], 
		'name_last': hamish['name_last'], 'u_id': hamish['u_id']}
		],
	}
	)
#Checks that the token has the correct authorization to add an owner
#(owner of slackr will by default be an owner of channel)

#Check that if there is a new user and they don't join a channel, that channel will not be in their channel list  
dummy_token = auth_register("Yeshey@hotmail.com", 'itsmepaswird', 'boop', 'ilast')
dummy = token_check(dummy_token['token'])
def test_channels_list_zero():
	assert(channel_list(dummy['token']) == [])
	

#checks to make sure joined channel is returned 
def test_channels_list_correct(): 
	assert(channel_list(kelly['token']) == 
		[
		{
		'channel_id' : channel_id_kelly['channel_id'],
		'name': 'Kelly_channel'
		},
		])

#tests to make sure all joined channels are returned 
def test_channels_list_multiple(): 
	assert(channel_list(hamish['token']) == 
		[
		{
		'channel_id' : channel_id_hamish['channel_id'],
		'name': 'Hamish_channel'
		},
		{
		'channel_id' : channel_id_kelly['channel_id'],
		'name': 'Kelly_channel'
		},
		])

#list all of the channels available 
def test_channels_listall_joined(): 
	assert(channels_list_all(hamish['token']) == 
		[
		{
		'channel_id' : channel_id_hamish['channel_id'],
		'name': 'Hamish_channel'
		},
		{
		'channel_id' : channel_id_zach['channel_id'],
		'name': 'Zach_channel'
		},
		{
		'channel_id' : channel_id_kelly['channel_id'],
		'name': 'Kelly_channel'
		},
		])


def test_channel_leave_invalid():
	with pytest.raises(InputError):
		channel_leave(hamish['token'], 67430)
	with pytest.raises(AccessError):
		channel_leave(hamish['token'], channel_id_zach['channel_id'])
 
	
def test_channel_leave_valid():
	channel_leave(hamish['token'], channel_id_kelly['channel_id'])
	assert(channel_list(hamish['token']) == 
		[
		{
		'channel_id' : channel_id_hamish['channel_id'],
		'name': 'Hamish_channel'
		}
		])

def test_channel_invite_invalid():
	with pytest.raises(InputError):
		channel_invite(hamish['token'], 67430, kelly['u_id'])
		channel_invite(hamish['token'], channel_id_hamish['channel_id'], "jone")
	with pytest.raises(AccessError):
		channel_invite(kelly['token'], channel_id_kelly['channel_id'], zach['u_id'])
 
 # Now we test inviting to hamish's channel
def test_channel_invite_valid():
	channel_invite(zach['token'], channel_id_zach['channel_id'], hamish['u_id'])
	assert(channel_list(hamish['token']) == 
		[
		{
		'channel_id' : channel_id_hamish['channel_id'],
		'name': 'Hamish_channel'
		},
		{
		'channel_id' : channel_id_zach['channel_id'],
		'name': 'Zach_channel'
		}
		])

