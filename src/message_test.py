#import message
#import channels
#import channel
import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channels_create, channel_invite
from message import message_send, message_send_later, message_react
from db import get_messages_store
import datetime

#Assumptions
#All the inputs are valid
hayden_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(hayden_dict['token'], 'Hayden', True)
rob_dict = auth_register("rob@gmail.com", "paswword123", "Rob", "Ever")
#channel_invite(hayden_dict['token'], chan_id["channel_id"], rob_dict["u_id"])

message_id = message_send(hayden_dict['token'], chan_id['channel_id'], "Haydens Message")


def test_message_send():
    assert get_messages_store()['Messages'][0] == {
        'channel_id': chan_id["channel_id"], 
        'message_id': message_id['message_id'], 
        'user_id': hayden_dict['u_id'], 
        'message': 'Haydens Message', 
        'Reacts': [], 
        'time_created': get_messages_store()['Messages'][0]['time_created'], 
        'is_pinned': False}

def test_message_send_invalid_InputError():
    with pytest.raises(InputError):
        message_send(hayden_dict['token'], chan_id['channel_id'], "H"*1001)

def test_message_send_invalid_AccessError():
    with pytest.raises(AccessError):
        message_send(rob_dict['token'], chan_id['channel_id'], "Robs message")

message_id1 = message_send_later(hayden_dict['token'], chan_id['channel_id'], "Haydens Message later", datetime.datetime.now()+  datetime.timedelta(0,1))


def test_message_send_later():
    assert get_messages_store()['Messages'][1] == {
        'channel_id': chan_id["channel_id"], 
        'message_id': message_id1['message_id'], 
        'user_id': hayden_dict['u_id'], 
        'message': 'Haydens Message later', 
        'Reacts': [], 
        'time_created': get_messages_store()['Messages'][1]['time_created'], 
        'is_pinned': False}

def test_message_send_later_invalid_AccessError():
    with pytest.raises(AccessError):
        message_send_later(rob_dict['token'], chan_id['channel_id'], "Robs message",datetime.datetime(2020, 3, 28, 2, 9, 46, 184346))
        
def test_message_send_later_invalid_InputError():
    with pytest.raises(InputError):
        message_send_later(hayden_dict['token'], chan_id['channel_id'], "Hayens message",datetime.datetime(2020, 3, 28, 2, 9, 46, 184346))
print(get_messages_store()['Messages'])


def test_message_react_later_invalid_InputError1():
    with pytest.raises(InputError):
        message_react(hayden_dict['token'],1 , 1) 

def test_message_react_later_invalid_InputError2():
    with pytest.raises(InputError):
        message_react(hayden_dict['token'],message_id['message_id'] , 2) 

chan_id_check = channels_create(hayden_dict['token'], 'Hayden', True)
message_id_check = message_send(hayden_dict['token'], chan_id_check['channel_id'], "Haydens Message Check")
message_react(hayden_dict['token'],message_id_check['message_id'] , 1)

def test_message_react():
    assert get_messages_store()['Messages'][2]['Reacts'] == [{'u_id': hayden_dict['u_id'], 'react_id': 1}] 

def test_message_react_later_invalid_InputError3():
    with pytest.raises(InputError):
        message_react(hayden_dict['token'],message_id_check['message_id'] , 1)


print(get_messages_store()['Messages'][2]['Reacts'])
"""
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

"""
