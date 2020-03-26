
import jwt

from db import get_user_store, add_user, login, make_user
from db import login, make_user, channel_add_all_members, get_channel_store
from db import token_check, channel_check, u_id_check
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    channel_store = get_channel_store()
    user_store = get_user_store()
    user = token_check(token)
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append({"u_id": user["u_id"], "name_first": user['name_first'], "name_last" : user["name_last"]})    
    return {

    }  

def channel_details(token, channel_id):
    #store = get_channel_store()
    #new_dict = store["Channels"]
    channel_info = channel_check(channel_id)
    if "is_public" in channel_info:
        del channel_info["is_public"]
    return channel_info

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
    if channel_check(channel_id) == False:
        raise InputError
    channel_store = get_channel_store()
    for iterator in channel_store["Channels"]:
        if iterator['channel_id'] == channel_id:
            for members in iterator['owner_members']:
                if members["u_id"] == u_id:
                    raise InputError
    owner_user = token_check(token)
    for owner_check in channel_store["Channels"]:
        if owner_check['channel_id'] == channel_id:
            for owners in owner_check['owner_members']:
                if owners["u_id"] != owner_user["u_id"]:
                    #print(channel_store["Channels"])
                    #print(owner_user)
                    raise AccessError
    user_store = get_user_store()
    user = u_id_check(u_id)
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            channel["owner_members"].append({"u_id": user["u_id"], "name_first": user['name_first'], "name_last" : user["name_last"]})
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    if channel_check(channel_id) == False:
        raise InputError
    channel_store = get_channel_store()
    for iterator in channel_store["Channels"]:
        if iterator['channel_id'] == channel_id:
            flag = 0
            for members in iterator['owner_members']:
                if members["u_id"] == u_id:
                    flag = 1
            if flag == 0:
                raise InputError
    owner_user = token_check(token)
    for owner_check in channel_store["Channels"]:
        if owner_check['channel_id'] == channel_id:
            second_flag = 0
            for owners in owner_check['owner_members']:
                if owners["u_id"] == owner_user["u_id"]:
                    second_flag = 1
            if second_flag == 0:
                raise AccessError
    user_store = get_user_store()
    user = u_id_check(u_id)
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            for member in channel["owner_members"]:
                if member["u_id"] == u_id:
                    channel["owner_members"].remove(member)
    return {
    }
    

        #{
       # 'channel_id'
       # 'owner_memmbers':[],
      #  'all_members':[],
      #  'is_public': Boolean
    #},

def channels_create(token, name, is_public):
    if len(name) > 20:
        raise InputError
    channel_dict = {
        'channel_id': name,
        'owner_members':[],
        'all_members':[],
        'is_public': is_public,
        'name' : name,
    }
    #user = token_check(token)
    store = get_channel_store()
    
    user_store = token_check(token)
    if user_store == None:
         raise InputError

    channel_dict['owner_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last']})
    
    channel_dict['all_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last']})
    
    store['Channels'].append(channel_dict)
    user_store['channel_id_owned'].append(channel_dict["channel_id"])
    user_store['channel_id_part'].append(channel_dict["channel_id"])
    return {
        'channel_id' : channel_dict["channel_id"]
    }

def channels_list_all(token):
    if token_check(token) == False:
        raise InputError
    channel_store = get_channel_store()
    return channel_store

def channel_list(token):
    if token_check(token) == False:
        raise InputError
    channel_store = get_channel_store()
    user = token_check(token)
    empty_list = []
    for channels in channel_store["Channels"]:
        for member in channels['all_members']:
            if member["u_id"] == user["u_id"]:
                empty_list.append({"channel_id" : channels["channel_id"], "name" : channels["name"]})
    return empty_list