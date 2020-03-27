from db import get_messages_store, get_user_store, get_channel_store, make_message
from db import token_check, channel_check, u_id_check, check_user_in_channel
from error import InputError, AccessError
from datetime import date, time, datetime

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
            message_id = make_message(message, channel_id, user['u_id'], time_sent)
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):

    return {
    }

def message_edit(token, message_id, message):
    return {
    }

