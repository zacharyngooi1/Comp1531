from db import get_messages_store, get_user_store, get_channel_store, make_message 
from db import member_channel_check, owner_channel_check
from db import token_check, channel_check, u_id_check, check_user_in_channel, message_check
from error import InputError, AccessError
from datetime import datetime 
import time

def message_send(token, channel_id, message):
    user = token_check(token)
    if user == False:  
        raise InputError
    channel = channel_check(channel_id)
    if channel == None: 
        raise InputError
    print(user['u_id'])
    #if check_user_in_channel(user['u_id'], channel_id) == False: 
    #    raise AccessError
    if (len(message) > 1000): 
        raise InputError
   # message_store = get_messages_store()
    print("hey", channel)
    for member in channel['all_members']: 
        if user['u_id'] == member['u_id']: 
            message_id = make_message(message, channel_id, user['u_id'], 0)
    
    return {
        'message_id': message_id, 
    }

def message_send_later(token, channel_id, message, time_sent): 
    user = token_check(token)
    if user == False:  
        raise InputError
    channel = channel_check(channel_id)
    if channel == False: 
        raise InputError
    if check_user_in_channel(user['u_id'], channel_id) == False: 
        raise AccessError
    if (len(message) > 1000): 
        raise InputError
    if(time_sent < datetime.now()): 
        raise InputError
    message_store = get_messages_store()
    for member in channel['all_members']: 
        if user['u_id'] == member['u_id']:
            #time.mktime(t.timetuple())

            wait_time = time_sent - datetime.now() 
            time.sleep(wait_time.total_seconds())
            #wait_time = time.mktime(datetime.datetime.now().timetuple()) - time.mktime(time_sent.timetuple())
            message_id = make_message(message, channel_id, user['u_id'], 0)
    return {
        'message_id': message_id,
    }


def message_react(token, message_id , react_id): 
    message = message_check(message_id)
    #print("This is message----->", message)
    if message == None:
        raise InputError
    if react_id != 1:   #This is assuming that there's only 1 react id (1)
        raise InputError   
    if message['react_id'] == react_id:
        raise InputError
    message['react_id'] = react_id
    return{

    }

def message_unreact(token, message_id , react_id): 
    message = message_check(message_id)
    #print("This is message----->", message)
    if message == None:
        raise InputError
    if react_id != 1:   #This is assuming that there's only 1 react id (1)
        raise InputError    
    if message['react_id'] != react_id:
        raise InputError
    message['react_id'] = 0
    return{

    }

def message_pin(token, message_id): 
    message = message_check(message_id)
    if message == None:
        raise InputError
    if owner_channel_check(token, message['channel_id']) == False:
        raise InputError
    if member_channel_check(token, message['channel_id']) == False:
        raise AccessError
    if message['is_pinned'] == True:
        raise InputError
    message['is_pinned'] = True
    return {

    }


def message_unpin(token, message_id): 
    message = message_check(message_id)
    if message == None:
        raise InputError
    if owner_channel_check(token, message['channel_id']) == False:
        raise InputError
    if member_channel_check(token, message['channel_id']) == False:
        raise AccessError    
    if message['is_pinned'] == False:
        raise InputError    
    message['is_pinned'] = False 
    return {

    }
def message_remove(token, message_id):
    message = message_check(message_id)
    if message == None:
        raise InputError
    is_owner = owner_channel_check(token, message['channel_id'])
    user = token_check(token)
    if user == None:
        raise AccessError

    is_sender = False
    #print("message----->",message)
    if user['u_id'] == message['user_id']:
        is_sender = True

    if (is_owner or is_sender) == False:
        raise AccessError

    message_data = get_messages_store()
    message_data['Messages'].remove(message)
    return {
    }


def message_edit(token, message_id, edited_message):
    #print(" ")
    #print("debug-------->", message['message'])
    #print(" ")
    #print("")    
    message = message_check(message_id)
    if message == None:
        raise InputError
    is_owner = owner_channel_check(token, message['channel_id'])
    user = token_check(token)
    if user == None:
        raise AccessError

    is_sender = False
    #print("message----->",message)
    if user['u_id'] == message['user_id']:
        is_sender = True

    if (is_owner or is_sender) == False:
        raise AccessError

    message['message'] = edited_message
 
    #message_data = get_messages_store()
    #message_data['Messages'].remove(message)
    return {
    }
