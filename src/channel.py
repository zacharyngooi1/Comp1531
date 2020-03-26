
import jwt

from db import get_user_store, add_user, login, make_user
from db import login, make_user, channel_add_all_members, get_channel_store
from db import token_check, channel_check

def channel_invite(token, channel_id, u_id):
    #@Muffeed you should go back to auth_register and add another key in the dictionary called channel_ids
    #It will be something like return_dict['channel_ids'] = []
    for user in data['user']:
        if user['token'] == token:
            if user['u_id'] == u_id:
                user['channel_ids'].append(channel_id)
    return {
    }

def channel_details(token, channel_id):
    all_members = [] # A list with dictionaries of users
    owner_members = [] # A list with dictionaries of users
    user_info_dictionary = {}
    for user in data['user']:
        for a_channel_id in user['channel_ids']:
            if a_channel_id == channel_id:
                all_members.append({
                        'u_id': user["u_id"], 
                        'name_first': user["name_first"], 
                        'name_last': user["name_last"],
                    })
            
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
	return { 
	} 

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }

        #{
       # 'channel_id'
       # 'owner_memmbers':[],
      #  'all_members':[],
      #  'is_public': Boolean
    #},

def channel_create(token, name, is_public):
    channel_dict = {
        'channel_id': name,
        'owner_members':[],
        'all_members':[],
        'is_public': is_public
    }
    #user = token_check(token)
    store = get_channel_store()
    
    user_store = token_check(token)
    if user_store == None:
         raise InputError

    channel_dict['owner_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last']})
    
    channel_dict['all_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last']})
    
    store['Channels'].append(channel_dict)


