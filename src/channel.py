
import jwt
from db import get_user_store, add_user, login, make_user
from db import login, make_user, get_channel_store, get_messages_store
from db import token_check, channel_check, u_id_check
from error import InputError, AccessError
from random import randrange


def channel_invite(token, channel_id, u_id):

    if channel_check(channel_id) == None:
        raise InputError

    if u_id_check(u_id) == False:
        return InputError

    if check_if_user_in_channel_member(token, channel_id) == True:
        raise AccessError

    
    channel_store = get_channel_store()
    user = token_check(token)
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append({"u_id": user["u_id"], "name_first": user['name_first'], "name_last" : user["name_last"]})    
    
    user['channel_id_part'].append(channel_id)

    return {} 

def channel_details(token, channel_id):
    if channel_check(channel_id) == None:
        raise InputError
    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    dict = {
    }
    channel_info = channel_check(channel_id)
    dict['name'] = channel_info['name']
    dict['owner_members'] = channel_info['owner_members']
    dict['all_members'] = channel_info['all_members']
    return dict

def channel_messages(token, channel_id, start):

    if channel_check(channel_id) == None:
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
    for x in message_store['Messages']:
        if x['channel_id'] == channel_id:
            proto_dict['messages'].append(x['message'])

    # Now i reverse the list to get the most recent message as the first value
    proto_dict['messages'].reverse()

    for i in range(50):
        for y in proto_dict['messages']:
            final_dict['messages'].append(y[start + i])
            final_dict['start'] = start
            final_dict['end'] = start + 50
            if start + 50 >= sum_of_messages:
                final_dict['end'] = -1

    return final_dict

def channel_leave(token, channel_id):
    if channel_check(channel_id) == None:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    channel = channel_check(channel_id)
    user = token_check(token)
    for inner in channel['all_members']:
        if inner['u_id'] == user['u_id']:
            channel['all_members'].remove(inner)

    for leave in user['channel_id_part']:
        if leave == channel_id:
            user['channel_id_part'].remove(leave)
    return {}


def channel_join(token, channel_id):

    if channel_check(channel_id) == None:
        raise InputError

    if (check_if_channel_is_public(channel_id) == True and 
    check_if_user_in_channel_owner(token, channel_id) == False):
        raise AccessError
    
    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    user = token_check(token)

    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append({"u_id": user["u_id"], 
            "name_first": user['name_first'], "name_last" : user["name_last"]})

    user['channel_id_part'].append(channel_id)

    return {} 


def channel_addowner(token, channel_id, u_id):
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == True:
        raise InputError

    if check_if_user_in_channel_owner(token, channel_id) == False:
        raise AccessError

    channel_store = get_channel_store()
    user = u_id_check(u_id)

    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            channel["owner_members"].append({"u_id": user["u_id"],
             "name_first": user['name_first'], "name_last" : user["name_last"]})

    user['channel_id_owned'].append(channel_id)
    user['channel_id_part'].append(channel_id)
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner(token, channel_id) == False:
        raise AccessError

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

    if len(name) > 20:
        raise InputError

    channel_dict = {
        'channel_id': len(name) + len(token) + randrange(25000),
        'owner_members':[],
        'all_members':[],
        'is_public': is_public,
        'name' : name,
        'standup' : {'is_standup_active':False, 'time_standup_finished':None, "standup_message":""}
    }

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


#####################################
##        Checker functions        ##
#####################################

def check_if_user_in_channel_member(token, channel_id):
    user = token_check(token)
    channel_store = get_channel_store()
    result = False
    for mem_check in channel_store["Channels"]:
        if mem_check['channel_id'] == channel_id:
            for mem in mem_check['all_members']:
                if mem["u_id"] == user["u_id"]:
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
        if pub['channel_id'] == channel_id:
            if pub['is_public'] == True:
                result = True
    return result