import message
import channels
import channel
import pytest
from error import InputError
from auth import auth_register

#Assumptions
#All the inputs are valid
def user_register(email, password, name_first, name_last):
	tmp = auth_register(email, password, name_first, name_last)    
	return {
        'u_id': tmp['u_id'],
        'token': tmp['token'],
		'name_first': name_first,
		'name_last': name_last, 
		'email': email,
		'password': password
    }

#Function to create a new channel. Returns information about that channel 
def new_channel(token, name, is_public): 
	tmp = channels_create(token, name, is_public)
	return { 
		'channel_id': tmp['channel_id'],
		'token': token,
		'name': name,
		'is_public': is_public
	}

#Checks weather the message has been sent
def test_message_send():
    #by default message_id is 1.
    user_results = user_register('email@email.com', 'Password', 'Citzen', 'Good')
    results = new_channel(user_results['token'], 'Test', True)

    #send a message
    message_id = message.message_send(12345, 1, 'Hello world')
    #check if the message has actually been sent
    message_log = channel.channel_messages(12345,1,0)
    flag =0
    for i in message_log['messages']:
        if i['message_id'] ==  message_id:
            flag = 1 
    assert flag == 1  
    
#Checks weather the message has been removed
def test_message_remove():
    #by default message_id is 1.
    user_results = user_register('email@email.com', 'Password', 'Citzen', 'Good')
    results = new_channel(user_results['token'], 'Test', True)

    #send on channel 1
    message_id = message.message_send(12345, 1, 'Hello world')
    #check if the function outputs the correct output
    assert message.message_remove(12345,message_id) == {}
    message_log = channel.channel_messages(12345,1,0)
    flag =0
    for i in message_log['messages']:
        if i['message_id'] ==  message_id:
            flag = 1 
    assert flag ==0

#Checks weather the message has been edited
def test_message_edit():
    user_results = user_register('email@email.com', 'Password', 'Citzen', 'Good')
    results = new_channel(user_results['token'], 'Test', True)

    #send on channel 1
    message_id = message.message_send(12345, 1, 'Bye world')

    message_id = message.message_edit(12345, 1, 'Hello world')
    #check if the message has been edit
    message_log = channel.channel_messages(12345,1,0)
    for i in message_log['messages']:
        if i['message_id'] ==  message_id and i['message'] == "Hello world":
            flag = 1 
    assert flag == 1
    
def test_message_except():
    #an example of when there would be an inout error ie. message longer than 1000
    with pytest.raises(InputError) as e:
        assert message.message_send(12345, 1, 'a'*1001)
    
    #Access error example
    #if someone called Bob tries to access channel    
    list_of_channels = channels_listall(12345)
    flag =1
    if "Bob" in list_of_channels[name]:
        flag = 0
    with pytest.raises(AccessError) as e:
        assert flag == 1
