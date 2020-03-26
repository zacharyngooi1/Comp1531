import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
import jwt
import hashlib

USERDATASTORE = {
    'user': [
    ],
    'Channel': [ 
    ],
    'Messages':[
    ],
}


def get_user_store():
    global USERDATASTORE
    return USERDATASTORE


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
        }

def add_user(email, password, name_first, name_last):
    store = get_user_store()
    u_id = len(store['user'])
    permission_id = permission_ids['SLACKR_OWNER'] if u_id == 0 else permission_ids['SLACKR_MEMBER']
    user = make_user(email, password, name_first, name_last, u_id, permission_id)
    store['user'].append(user)
    return user


def login(user):
    SECRET = 'abcde'
    token = str(jwt.encode({'handle_str': user['handle_str']}, SECRET, algorithm='HS256'))
    logged_in_users[token] = user
    return token





