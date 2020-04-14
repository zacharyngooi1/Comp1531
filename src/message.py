from db import get_messages_store, get_user_store, get_channel_store, make_message 
from db import member_channel_check, owner_channel_check, react_check, member_channel_check
from db import token_check, channel_check, u_id_check, check_user_in_channel, message_check
from error import InputError, AccessError
import datetime
from datetime import timezone
import time
from auth import auth_register
from hangman import play_hangman
#from auth import auth_register
#from channel import channels_create,channel_invite


def message_send(token, channel_id, message):
    """ Sends a message to the designated channel 

    Parameters:
        token (string)
        channel_id(int)
        message(string)
    
    Returns:
        (dictionary): A dictionary containing the message_id
        of the message that was sent.
    """
    
    user = token_check(token)
    if user == False:  
        raise InputError
    channel = channel_check(channel_id)
    if channel == None: 
        raise InputError
    #if check_user_in_channel(user['u_id'], channel_id) == False: 
    #    raise AccessError
    if (len(message) > 1000): 
        raise InputError
    if member_channel_check(token, channel_id) == False:
        raise AccessError
   # message_store = get_messages_store()
    for member in channel['all_members']: 
        if user['u_id'] == member['u_id']: 
            message_id = make_message(message, channel_id, user['u_id'], 0)
    if message == "/hangman":
        channel['Hangman']['is_hangman_active'] = True
    
    if message[0:6] == "/guess" and channel['Hangman']['is_hangman_active'] == True:
        
        #print(play_hangman(message[7]))
        hangman = play_hangman(message[7])
        make_message(hangman['hang_man_drawing']+hangman['current_word'], channel_id, user['u_id'], 0)
    return {
        'message_id': message_id,
    }

def message_send_later(token, channel_id, message, time_sent): 
    """ Sends a message to the designated channel at a specified time

    Parameters:
        token (string)
        channel_id(int)
        message(string)
        time_sent (datetime)
    
    Returns:
        (dictionary): A dictionary containing the message_id
        of the message that was sent.
    """
 
    user = token_check(token)
    if user == False:  
        raise InputError
    channel = channel_check(channel_id)

    if channel == False: 
        raise InputError

    if member_channel_check(token, channel_id) == False: 
        raise AccessError
    if (len(message) > 1000): 
        raise InputError

  
    #should this maybe be more ??
    if int(time_sent) < int(datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()): 
       
        raise InputError
    message_store = get_messages_store()
   
    for member in channel['all_members']: 
       
        if user['u_id'] == member['u_id']:
            
         
            
            wait_time = time_sent - datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp() 
            time.sleep(wait_time)
            #wait_time = time.mktime(datetime.datetime.now().timetuple()) - time.mktime(time_sent.timetuple())
            message_id = make_message(message, channel_id, user['u_id'], 0)
       
    return {
        'message_id': message_id,
    }


def message_react(token, message_id , react_id): 
    """ Reacts to a message  

    Parameters:
        token (string)
        message_id(int)
        react_id(int)
    
    """
    message = message_check(message_id)
  
    if message == None:
        
        raise InputError
    if react_id != 1:   #This is assuming that there's only 1 react id (1)
       
        raise InputError   

    user = token_check(token)
    if user == None:
        
        raise AccessError
    
    if react_check(message_id, user['u_id'], react_id):
        print("react check input errroorrrrrrrr")
        raise InputError

    is_this_user_reacted = False;

    flag = 0
    for reacts in message['reacts']:
        if reacts['react_id'] == react_id:
            reacts['u_ids'].append(int(user['u_id']))
            flag = 1
            if reacts['is_this_user_reacted']:
                is_this_user_reacted = True

    if message['user_id'] == user['u_id']:
        is_this_user_reacted = True
        
    if flag ==0:    
        dict_append  = { 'u_ids': [int(user['u_id'])], 'react_id' : int(react_id), 'is_this_user_reacted' : is_this_user_reacted  }
        message['reacts'].append(dict_append)
    return{
    }

def message_unreact(token, message_id , react_id): 
    """ Removes a react from a message  

    Parameters:
        token (string)
        message_id(int)
        react_id(int)
    
    """
    message = message_check(message_id)
    #print("This is message----->", message)
    if message == None:
        raise InputError
    if react_id != 1:   #This is assuming that there's only 1 react id (1)
        raise InputError    
    user = token_check(token)
    if user == None:
        raise AccessError
    
    if react_check(message_id, user['u_id'], react_id) == False:
        raise InputError

    flag = 0 
    for reacts in message['reacts']:
        if reacts['react_id'] == react_id:
            if user['u_id'] in reacts['u_ids']:
                reacts['u_ids'].remove(user['u_id'])
                if len(reacts['u_ids']) == 0:
                    flag = 1

    if flag == 1:
        #dict_append  = { 'u_ids': user['u_id'], 'react_id' : react_id  }
        
        for react in message['reacts']:
            if react_id == react['react_id']:
                break
        message['reacts'].remove(react)
    return{

    }

def message_pin(token, message_id): 
    """ Pins a message  

    Parameters:
        token (string)
        message_id(int)
    
    """
    message = message_check(message_id)
    if message == None:
        raise InputError
    if member_channel_check(token, message['channel_id']) == False:
        raise AccessError
    if owner_channel_check(token, message['channel_id']) == False:
        raise AccessError
    if message['is_pinned'] == True:
        raise InputError
    message['is_pinned'] = True
    return {

    }


def message_unpin(token, message_id): 
    """Unpins a message  

    Parameters:
        token (string)
        message_id(int)
    
    """
    message = message_check(message_id)
    if message == None:
        raise InputError
    if member_channel_check(token, message['channel_id']) == False:
        raise AccessError 
    if owner_channel_check(token, message['channel_id']) == False:
        raise InputError   
    if message['is_pinned'] == False:
        raise InputError    
    message['is_pinned'] = False 
    return {

    }
def message_remove(token, message_id):
    """Removes a message  

    Parameters:
        token (string)
        message_id(int)
    
    """
    message = message_check(message_id)
    if message == None:
        raise InputError
    is_owner = owner_channel_check(token, message['channel_id'])
    user = token_check(token)
    if user == False:
        raise AccessError

    is_sender = False
    #print("message----->",message)
    if user['u_id'] == message['user_id']:
        is_sender = True

    print('is owner: ', is_owner,'is_sender:', is_sender)
    if (is_owner or is_sender) == False:
        raise AccessError

    message_data = get_messages_store()
    message_data['Messages'].remove(message)
    return {
    }


def message_edit(token, message_id, edited_message):
    """Edits a current message  

    Parameters:
        token (string)
        message_id(int)
        edited_message(string)
    
    """
    message = message_check(message_id)
    if message == None:
        raise InputError
    is_owner = owner_channel_check(token, message['channel_id'])
    user = token_check(token)
    if user == False:
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


