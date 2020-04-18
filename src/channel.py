import jwt
from db import get_user_store, add_user, login, make_user
from db import login, make_user, get_channel_store, get_messages_store, get_user_store
from db import token_check, channel_check, u_id_check, member_channel_check
from error import InputError, AccessError
from random import randrange
from datetime import timezone

def channel_invite(token, channel_id, u_id):

    ''' Invites a user to join a channel that they are not already in
    
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            u_id (int): unique user identification
       
    '''

    if not channel_check(channel_id):
        raise InputError

    if not u_id_check(u_id):
        return InputError

    if check_if_user_in_channel_member_uid(u_id, channel_id):
        raise AccessError

    channel_store = get_channel_store()
    user = u_id_check(u_id)
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append({"u_id": user["u_id"], "name_first": user['name_first'], "name_last" : user["name_last"], 'profile_img_url': user['profile_img_url']})    
    
    user['channel_id_part'].append(channel_id)

    return {} 

def channel_details(token, channel_id):
    '''Provides user with the basic information of a channel, given channel id, if 
    user is part of channel.
    
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
        
        Returns: 
            (dict): returns details about channel 
    
    '''
    if channel_check(channel_id) == False:
        raise InputError
    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    ch_dict = {
    }
    channel_info = channel_check(channel_id)
    ch_dict['name'] = channel_info['name']
    ch_dict['owner_members'] = channel_info['owner_members']
    ch_dict['all_members'] = channel_info['all_members']
    return ch_dict

def channel_messages(token, channel_id, start):
    '''Returns a range of 50 messages in a channel, if user is part of that channel.
   
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            start (int): which message wants to start range at 
        
        Returns: 
            (list): returns list of messages from channel 
    '''
   
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError
    
    sum_of_messages = 0
    
    message_store = get_messages_store()
    
    for x in message_store['Messages']:
            if x['channel_id'] == channel_id:
                sum_of_messages += 1
    
    if start > sum_of_messages:
        raise InputError

    proto_dict = {
        'messages':[]
    }

    final_dict = {
        'messages':[]
    }
    proto_dict = get_messages_store()['Messages']
   
    counter = 0
    if len(proto_dict) != 0:
        #print('in the if loop aye ')
        for message in reversed(proto_dict):
  
            if int(message['channel_id']) == int(channel_id):
             
                if counter >= start:
                  
                    dict_to_app = {
                        'message_id':message['message_id'],
                        'u_id': message['user_id'],
                        'message': message['message'],
                        'time_created': message['time_created'].replace(tzinfo=timezone.utc).timestamp(),
                        'reacts': message['reacts'],
                        'is_pinned': message['is_pinned']
                        
                    }
                    final_dict['messages'].append(dict_to_app)    
                counter = counter + 1
            if counter >= 50:
                counter = -1
                break
    
    final_dict['start'] = start
    final_dict['end'] = counter

    return final_dict


def channel_leave(token, channel_id):
    '''Removes member from a channel.

        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
    '''

  
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    channel = channel_check(channel_id)
    
    user = token_check(token)
    
    for inner in channel['all_members']:
        if int(inner['u_id']) == int(user['u_id']):
           
            channel['all_members'].remove(inner)
         

    for leave in user['channel_id_part']:
       
        if int(leave) == int(channel_id):
       
            user['channel_id_part'].remove(leave)
        
    return {}


def channel_join(token, channel_id):
    '''Adds a member to a channel.
    
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
        
    '''
    if channel_check(channel_id) == False:
    
        raise InputError

    if (check_if_channel_is_public(channel_id) == False or
    check_if_user_in_channel_member(token, channel_id) == True):
       
        raise AccessError
 

    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    user = token_check(token)

    for channel in channel_store["Channels"]:
        #print("gets in for loop")
        if channel["channel_id"] == int(channel_id):
            #print("gets in if statement")
            channel["all_members"].append({"u_id": user["u_id"], 
            "name_first": user['name_first'], "name_last" : user["name_last"], 'profile_img_url': user['profile_img_url']})

    user['channel_id_part'].append(channel_id)

    return {} 


def channel_addowner(token, channel_id, u_id):
    '''Adds someone as owner to a channel.
   
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            u_id (int): user identification 
        
    '''
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == True:
        raise InputError
    
    permission_error = token_check(token)

    if check_if_user_in_channel_owner(token, channel_id) == False:
        if permission_error['permission_id'] != 1:
            raise AccessError
        else:
            pass

    
    channel_store = get_channel_store()
    user = u_id_check(u_id)

    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            if member_channel_check(user['token'], channel_id) == False:
                channel["all_members"].append({"u_id": user["u_id"],
             "name_first": user['name_first'], "name_last" : user["name_last"]})
            channel["owner_members"].append({"u_id": user["u_id"],
             "name_first": user['name_first'], "name_last" : user["name_last"]})

            

    user['channel_id_owned'].append(channel_id)
    user['channel_id_part'].append(channel_id)
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    '''Removes someone from owner to a channel.
   
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            u_id (int): user identification 
        
    '''
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == False:
        raise InputError

    permission_error = token_check(token)

    if check_if_user_in_channel_owner(token, channel_id) == False:
        if permission_error['permission_id'] != 1:
            raise AccessError
        else:
            pass

    user = u_id_check(u_id)
    channel_store = get_channel_store()
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            for member in channel["owner_members"]:
                if member["u_id"] == u_id:
                    channel["owner_members"].remove(member)

    for leave in user['channel_id_owned']:
        if leave == channel_id:
            user['channel_id_owned'].remove(leave)

    return {}

def channels_create(token, name, is_public):
    '''Creates a new channel.
   
        Parameters: 
            token (str): authorization hash 
            name (string): what channel will be named
            is_public (bool): true/false for public channel
        
        Returns: 
            (int): channel id 
        
    '''
    if len(name) > 20:
        raise InputError

    channel_dict = {
        'channel_id': int(len(name) + len(token) + randrange(25000)),
        'owner_members':[],
        'all_members':[],
        'is_public': bool(is_public),
        'name' : name,
        'standup' : {'is_standup_active':False, 'time_standup_finished':None, "standup_message":"", 'u_id_standup_started': 0, 'is_message_sent': True},
        'Hangman' : {'is_hangman_active': False, 'Guess':""}
    }

    store = get_channel_store()
    
    store1 = get_user_store
    user_store = token_check(token)
    
    if user_store == False:
         raise InputError(description="channel create user not found")

    channel_dict['owner_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last'], 'profile_img_url': user_store['profile_img_url']})
    
    channel_dict['all_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last'], 'profile_img_url': user_store['profile_img_url']})
    
    store['Channels'].append(channel_dict)
    user_store['channel_id_owned'].append(channel_dict["channel_id"])
    user_store['channel_id_part'].append(channel_dict["channel_id"])
    
    return {
        'channel_id' : channel_dict["channel_id"]
    }

def channels_list_all(token):
    '''Returns all channels.
    
        Parameters: 
            token (str): authorization hash 
        
        Returns: 
            (list):  list of channels
    '''
   
    if token_check(token) == False:
        raise InputError
   
    channel_store = get_channel_store()
    empty_list = []
   
    
    for channels in channel_store['Channels']:
        empty_list.append({"channel_id" : channels["channel_id"], "name" : channels["name"]})
    return {'channels':empty_list}

def channel_list(token):
    '''Lists channels a user is apart of.

        Parameters: 
            token (str): authorization hash 
            name (string): what channel will be named
            is_public (bool): true/false for public channel
        
        Returns: 
            (int): channel id 
    '''
   
    if token_check(token) == False:
       
        raise InputError
    channel_store = get_channel_store()
    user = token_check(token)
    empty_list = []
    for channels in channel_store["Channels"]:
        for member in channels['all_members']:
            if member["u_id"] == user["u_id"]:
                empty_list.append({"channel_id" : channels["channel_id"], "name" : channels["name"]})
    return {'channels':empty_list}


#####################################
##        Checker functions        ##
#####################################
def check_if_channel_exists(channel_id):
    channel_store = get_channel_store()
    result = False
    for id in channel_store['Channels']:
        if id['channel_id'] == int(channel_id):
            result = True
    return result

def check_if_user_in_channel_member(token, channel_id):
    user = token_check(token)
    channel_store = get_channel_store()
    result = False

   
    for mem_check in channel_store["Channels"]:
       
        if int(mem_check['channel_id']) == int(channel_id):
          
            for mem in mem_check['all_members']:
               
                if int(mem["u_id"]) == int(user["u_id"]):
                    
                    result = True
    return result

def check_if_user_in_channel_owner(token, channel_id):
    user = token_check(token)
    channel_store = get_channel_store()
    result = False
    for mem_check in channel_store["Channels"]:
        if mem_check['channel_id'] == channel_id:
            for mem in mem_check['owner_members']:
                if mem["u_id"] == user["u_id"]:
                    result = True
    return result

def check_if_user_in_channel_owner_uid(u_id, channel_id):
    channel_store = get_channel_store()
    result = False
    for mem_check in channel_store["Channels"]:
        if mem_check['channel_id'] == channel_id:
            for mem in mem_check['owner_members']:
                if mem["u_id"] == u_id:
                    result = True
    return result

def check_if_user_in_channel_member_uid(u_id, channel_id):
    channel_store = get_channel_store()
    result = False
    for mem_check in channel_store["Channels"]:
        if mem_check['channel_id'] == channel_id:
            for mem in mem_check['all_members']:
                if mem["u_id"] == u_id:
                    result = True
    return result

def check_if_channel_is_public(channel_id):
    channel_store = get_channel_store()
    result = False
    for pub in channel_store['Channels']:
        
        if pub['channel_id'] == int(channel_id):
          
            if pub['is_public'] == True:
                result = True
    return result
