import sys
from json import dumps
from flask import Flask, request
#from flask_cors import CORS
import jwt
import hashlib
import re
from datetime import date, time, datetime
from random import randrange

USERDATASTORE = {
    'users': []
}


CHANNELSTORE = {
    'Channels': [
        #{
       # 'channel_id'
       # 'owner_memmbers':[],
      #  'all_members':[],
      #  'is_public': Boolean
    #},
    ]
}

MESSAGESTORE = { 
    'Messages': [
        #{
            #channel_id
            #message_id
            #user_id
            #message
            #react_id
            #is_pinned
            #time_created
        #}
    ]
}

PERMISSIONSTORE = {
    "SLACKR_OWNER": 1,
    "SLACKR_MEMBER": 2,
    "CHANNEL_OWNER": 1,
    "CHANNEL_MEMBER": 2,
}

def get_user_store():
    global USERDATASTORE
    return USERDATASTORE

def get_channel_store():
    global CHANNELSTORE
    return CHANNELSTORE

def get_messages_store():
    global MESSAGESTORE
    return MESSAGESTORE

def get_permission_store():
    global PERMISSIONSTORE
    return PERMISSIONSTORE

def make_message(message, channel_id, user_id, time_created): 
    store = get_messages_store()
    user = u_id_check(user_id)
    react_id = 0 #assume the message isn't reacted
    message_id = len(message) #PLACEHOLDER same as channel id 
    #maybe make message_id a global variable 
    if time_created == 0: 
        time = datetime.now()
    else: 
        time = time_created
    user['messages_created'].append(message)
    store['Messages'].append({'channel_id':channel_id, 'message_id':message_id, 'user_id': user_id, 'message': message, 'react_id': react_id, 'time_created': time, 'is_pinned' : False})
    return message_id

def check_user_in_channel(u_id, channel_id): 
    channel_data = get_channel_store
    print(channel_data)
    channel = channel_check(channel_id)
    flag = 0
    for member in channel_iter['all_members']: 
        if member['u_id'] == u_id: 
            flag = 1
    if flag == 1: 
        return True
    else: 
        return False
    
                

"""
channels.append(ch)


add_channel(creator: User)


creator.channels_joined.append(ch)


ch = make_channel(...)


ch = get_ch_from_id(channel_id)


if ch in usr['channels_owned']:
   # stuff

"""






logged_in_users = {}
permission_ids = {
    "SLACKR_OWNER": 1,
    "SLACKR_MEMBER": 2,
    "CHANNEL_OWNER": 1,
    "CHANNEL_MEMBER": 2,
}

def make_user(email, password, name_first, name_last, u_id, perm_id):

    return {
            'u_id': u_id,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': (name_first[0]+name_last).lower(),
            'email': email,
            'password': password,
            'permission_id': perm_id,
            'channel_id_owned': [],
            'channel_id_part': [],
            'messages_created':[],
        }

def add_user(email, password, name_first, name_last):
    store = get_user_store()
    u_id = len(name_first) +len(name_last) +len(email) + randrange(100000)
    permission_id = permission_ids['SLACKR_OWNER'] if u_id == 0 else permission_ids['SLACKR_MEMBER']
    user = make_user(email, password, name_first, name_last, u_id, permission_id)
    store['users'].append(user)
    return user


def login(user):
    SECRET = 'abcde'
    token = str(jwt.encode({'handle_str': user['handle_str']}, SECRET, algorithm='HS256'))
    logged_in_users[token] = user
    return token

#Standup helper functions
def is_any_other_standup_active(channel_id):
    channel_store = get_channel_store()
    for channel in channel_store['Channels']:
        if channel['channel_id'] != channel_id:
            if channel['standup']['is_standup_active'] == True:
                return True
    return False


###################################################
##             Checking functions                ##
###################################################

def u_id_check(u_id):
    data = get_user_store()
    for user in data['users']:
        if user['u_id'] == u_id:
            return user
    return False
    
def handle_check(handle_str):
    data = get_user_store()
    for user in data['users']:
        if user['handle_str'] == handle_str:
            return True
    return False
    
# Make a regular expression 
# for validating an Email 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def email_check(email):
    # pass the regualar expression
    # and the string in search() method
    if (re.search(regex, email)):
        return True
    else:
        return False
    
def email_dupe_check(email):
    data = get_user_store()
    for user in data['users']:
        if user['email'] == email:
            return True
    return False

def token_check(token):
    data = get_user_store()
    for user in data['users']:
        if user['token'] == token:
            return user
    return False

def channel_check(channel_id):
    data = get_channel_store()
    flag = 0
    #print(channel_id)
    for channel in data['Channels']:
        if channel['channel_id'] == channel_id:
            #print("Hey")
            return channel
    #print("False")
    return None

def password_check(password):
    data = get_user_store()
    for user in data['users']:
        if user['pasword'] == password:
            return user
    return False


def message_check(message_id):
    data = get_messages_store()
   
    for message in data['Messages']:
        #print("data---------->",message_id['message_id'])
        if message['message_id'] == message_id['message_id']:
            return message
    return None

def owner_channel_check(token, channel_id):
    user = token_check(token)   #checks if it's a valid user
    if user == None:
        raise AccessError

    channel = channel_check(channel_id)
    if user == None:
        raise AccessError

    for member in channel['owner_members']:     
        if member['u_id'] == user['u_id']:
            return True
    return False




def member_channel_check(token, channel_id):
    user = token_check(token)   #checks if it's a valid user
    if user == None:
        raise AccessError
    channel = channel_check(channel_id)
    if user == None:
        raise AccessError

    for member in channel['all_members']:
        if member['u_id'] == user['u_id']:
            return True
    return False

    
    
    
