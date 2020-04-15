import sys
from json import dumps
from flask import Flask, request
import jwt
import hashlib
import re
import string
import random
from datetime import date, time, datetime, timezone
from random import randrange

USERDATASTORE = {
    'users': [
        #profile_img_url: ""
    ]
}


CHANNELSTORE = {
    'Channels': [
        #{
        #'channel_id'
        #'owner_memmbers':[],
        #'all_members':[],
        #'is_public': Boolean
        # 'standup' : {'is_standup_active':False, 'time_standup_finished':None, 'standup_message':"", 'u_id_standup_started': 0}
    #},
    ],
}

MESSAGESTORE = { 
    'Messages': [
        #{
            #channel_id
            #message_id
            #user_id
            #message
            #reacts[]  <--- contains dicts of people that reacted(user_id) and reaction_id
            #is_pinned
            #time_created
        #}
    ],
    
   
    
    
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

def reset_store():
    global USERDATASTORE
    global CHANNELSTORE
    global MESSAGESTORE
    USERDATASTORE = {
        'users' : []
    }
    CHANNELSTORE = {
        'Channels' : []
    }
    MESSAGESTORE = {
        'Messages' : []
    }

def make_message(message, channel_id, user_id, time_created): 
    store = get_messages_store()
    user = u_id_check(user_id)
    Reacts = []
    message_id = len(message) + randrange(25000)
    if time_created == 0: 
        time = datetime.utcnow()
        
    else: 
        time = time_created
    user['messages_created'].append(message)
    store['Messages'].append({'channel_id':channel_id, 'message_id':message_id, 'user_id': user_id, 'message': message, 'reacts': Reacts, 'time_created': time, 'is_pinned' : False})
    return message_id

def check_user_in_channel(u_id, channel_id): 
    channel_data = get_channel_store
   
    channel = channel_check(channel_id)
    flag = 0
    for member in channel_iter['all_members']: 
        if int(member['u_id']) == int(u_id): 
            
            flag = 1
    if flag == 1: 
        return True
    else: 
        return False

logged_in_users = {}

def get_logged_in_users():
    global logged_in_users
    return logged_in_users


PERMISSIONSTORE = {
    "SLACKR_OWNER": 1,
    "SLACKR_MEMBER": 2,
    "USER_NUM": [],
}

def make_user(email, password, name_first, name_last, u_id, perm_id):

    return {
            'u_id': u_id,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': create_handle(name_first, name_last),
            'email': email,
            'password': password,
            'permission_id': perm_id,
            'channel_id_owned': [],
            'channel_id_part': [],
            'messages_created':[],
            'profile_img_url': "",
        }

def create_handle(first_name, last_name):
   
    sample_handle = first_name[0] + last_name
    sample_handle = sample_handle.lower()

    if handle_check(sample_handle):
        sample_handle = sample_handle + randrange(25000)

    if len(sample_handle) > 20:
        sample_handle = sample_handle[0:20]

    return sample_handle

def add_user(email, password, name_first, name_last):
    permission = get_permission_store()
    store = get_user_store()
    u_id = len(name_first) +len(name_last) +len(email) + randrange(100000)
    if len(permission['USER_NUM'] == 0):
        permission['USER_NUM'].append(u_id)
        permission_id = permission['SLACKR_OWNER']
    else:
        permission_id = permission['SLACKR_MEMBER']
    user = make_user(email, password, name_first, name_last, u_id, permission_id)
    store['users'].append(user)
    return user


def login(user):
    SECRET = 'abcde'
    token = str(jwt.encode({'handle_str': user['handle_str']}, SECRET, algorithm='HS256'))
    logged_in_users[token] = user
    return token

#Standup helper functions
def message_create_for_standup(channel_id, u_id, message):
    user = u_id_check(u_id)
    channel = channel_check(channel_id)
    final_string = channel["standup"]["standup_message"]
    return_string = user['handle_str'] + ":" + message + '\n'
    channel["standup"]["standup_message"] = final_string + return_string
    
###################################################
##             Checking functions                ##
###################################################

def u_id_check(u_id):
    #print(u_id)
    data = get_user_store()
    for user in data['users']:
        if int(user['u_id']) == int(u_id):
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

def email_check(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
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
    data = logged_in_users

    if token in data:
        return data[token]

    return False

def channel_check(channel_id):
    data = get_channel_store()
    for channel in data['Channels']:
        if int(channel['channel_id']) == int(channel_id):
            return channel
    return False

def password_check(password):
    data = get_user_store()
    for user in data['users']:
        if user['password'] == password:
            return user
    return False


def message_check(message_id):
    data = get_messages_store()
   
    for message in data['Messages']:
        if int(message['message_id']) == int(message_id):
            return message
    return None

def owner_channel_check(token, channel_id):
    user = token_check(token)   #checks if it's a valid user
    if user == False:
        raise InputError

    channel = channel_check(channel_id)
    if channel == None:
        raise InputError

    for member in channel['owner_members']:     
        if int(member['u_id']) == int(user['u_id']):
            return True
    return False




def member_channel_check(token, channel_id):
    user = token_check(token)   #checks if it's a valid user
    if user == False:
        raise InputError
    channel = channel_check(channel_id)
    if channel == None:
        raise InputError

    for member in channel['all_members']:
        if int(member['u_id']) == int(user['u_id']):
            return True
    return False

    
def react_check(message_id, user_id, react_id):
    data = get_messages_store()
   
    for message in data['Messages']:
        if int(message['message_id']) == int(message_id):
            for reacts in message['reacts']:
                if int(reacts['react_id']) == int(react_id):
                    for users in reacts['u_ids']:
                        if int(users) == user_id:
                            return True
    return False


def find_email(email):
    data = get_user_store()
    for user in data['users']:
        if user['email'] == email:
            return user
    return False

def find_code(code):
    data = get_user_store()
   
    for user in data['users']:
      
        if 'reset' in user:
           
            if user['reset'] == code:
              
                return user
    return False
    
##derived from https://pynative.com/python-generate-random-string/

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
