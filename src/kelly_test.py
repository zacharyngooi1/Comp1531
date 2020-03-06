import pytest 
from channel import channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from auth import auth_register

#Function to create a new user. Returns information about that new user 
def user_register(email, password, name_first, name_last):
	tmp = auth_register(email, password, name_first, name_last)    
	return {
        'u_id': tmp['u_id'],
        'token': tmp['token'],
		'name_first': name_first,
		'name_last': name_last, 
		'email': email
		'password': password
    }

#Function to create a new channel. Returns information about that channel 
def new_channel(token, name, is_public): 
	tmp = channels_create(token, name, is_public)
	return { 
		'channel_id': tmp['channel_id']
		'token': token
		'name': name
		'is_public': is_public
	}

#Tests that you cannot join a channel with an invalid ID
def test_channel_join_id(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	#Edits the valid channel_id so that it is no invalid
	bad_id = results['channel_id'] += 6
	#Should raise an input error 
    with pytest.raises(InputError): 
        channel_join(user_results['token'], bad_id)

#Tests that a user (who is not an admin) can not join a private channel 
def test_channel_join_access(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	#Creates a new private channel 
	results = new_channel(user_results['token'], 'Test', False)
	with pytest.raises(AccessError): 
		channel_join(user_results['token'], results['channel_id']) 

#Tests to make sure a user can correctly join a channel 
def test_channel_join_correct(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	channel_join(user_results['token'], results['channel_id'])
	#chan_list is a dictionary of all of the channels that a user is apart of 
	chan_list = channels_list(user_results['token']) 
	#check to make sure that dictionary contains the channel you wanted to add them to 
	assert(chan_list.contains_key(results['channel_id']))

#Tests to make sure a user can correctly join a channel by checking to see if the dictionary for a new user is 1 after adding them to their first channel 
def test_channel_join_correct2(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	channel_join(user_results['token'], results['channel_id'])
	#chan_list is a dictionary of all of the channels that a user is apart of 
	chan_list = channels_list(user_results['token']) 
	#check to make sure that dictionary contains the channel you wanted to add them to 
	assert(len(chan_list) == 1)

#Tests that you cannot add an owner to a channel with an invalid ID
def test_channel_addowner_id(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	#Edits the valid channel_id so that it is no invalid
	bad_id = results['channel_id'] += 6
	#Should raise an input error 
    with pytest.raises(InputError): 
        channel_addowner(user_results['token'], bad_id, user_results['u_id'])

#Checks the the user is not already an owner 
def test_channel_addowner_owner(): 
	

#Checks that the token has the correct authorization to add an owner

 
#Tests that you cannot remove an owner to a channel with an invalid ID
def test_channel_removeowner_id(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	#Edits the valid channel_id so that it is no invalid
	bad_id = results['channel_id'] += 6
	#Should raise an input error 
    with pytest.raises(InputError): 
        channel_removeowner(user_results['token'], bad_id, user_results['u_id'])

#Checks the the user is not already not in list 

#Checks that token has correct authorization to remove 

#Check that if there is a new user and they don't join a channel, that channel will not be in their channel list  
def test_channels_list_zero():
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	chan_list = channels_list(user_results['token']) 
	assert(chan_list.contains_key(results['channel_id']) == false)  

def test_channels_list_correct(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	channel_join(user_results['token'], results['channel_id'])
	#chan_list is a dictionary of all of the channels that a user is apart of 
	chan_list = channels_list(user_results['token']) 
	#check to make sure that dictionary contains the channel you wanted to add them to 
	assert(chan_list.contains_key(results['channel_id']))

def test_channels_list_multiple(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	results2 = new_channel(user_results['token'], 'Test2', True)
	channel_join(user_results['token'], results['channel_id'])
	channel_join(user_results['token'], results2['channel_id'])
	#chan_list is a dictionary of all of the channels that a user is apart of 
	chan_list = channels_list(user_results['token']) 
	#check to make sure that dictionary contains the channel you wanted to add them to 
	assert(chan_list.contains_key(results['channel_id']) and chan_list.contains_key(results2['channel_id']))

#list all of the channels that the user has joined 
def test_channels_listall_joined(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	channel_join(user_results['token'], results['channel_id'])
	#chan_list is a dictionary of all of the channels that a user is apart of 
	chan_list = channels_listall(user_results['token']) 
	#check to make sure that dictionary contains the channel you wanted to add them to 
	assert(chan_list.contains_key(results['channel_id']))

#make sure the user cannot see any channels that are private/that they are not authorized to see 
def test_channels_listall_private(): 
 
#list all of the public channels that the user has not joined 
def test_channels_listall_notjoinedpublic(): 
	user_results = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
	results = new_channel(user_results['token'], 'Test', True)
	channel_join(user_results['token'], results['channel_id'])
	#chan_list is a dictionary of all of the channels that a user is apart of 
	chan_list = channels_listall(user_results['token']) 
	#check to make sure that dictionary contains the channel you wanted to add them to 
	assert(chan_list.contains_key(results['channel_id']))	


	
 
	
