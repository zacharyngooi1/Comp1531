import jwt
import hashlib
from json import dumps
from flask import Flask, request
from db import get_user_store, add_user, login, make_user,get_channel_store, get_messages_store
from db import token_check, channel_check, email_check, email_dupe_check, password_check
from channel import channels_create, channel_details, channel_invite, channel_addowner
from channel import channel_removeowner, channels_list_all, channel_list, channel_leave, channel_join
from message import message_send, message_send_later, message_react, message_unreact, message_pin, message_unpin
from message import message_remove, message_edit
from error import InputError, AccessError
from datetime import datetime

def sendSuccess(data):
    return dumps(data)

def sendError(message):
    return dumps({
        '_error' : message,
    })

#Assumption: Assume there are no users with the same firstname + lastname + first letter of their password
def auth_register(email, password, name_first, name_last):
    if email_check(email) == False:
        raise InputError
    if email_dupe_check(email) == True:
        raise InputError
    if len(password) < 6:
        raise InputError
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError
    user = add_user(email, password, name_first, name_last)
    token = login(user)
    data = get_user_store()
    for i in data['users']:
        if i['u_id'] == user['u_id']:
            i['token'] = token
    return {
        "u_id": user["u_id"],
        "token": token
    }

def auth_logout(token):
    data = get_user_store()
    for user in data['users']:
        if user['token'] == token:
            user.pop('token')
            return True
    return False
    
def auth_login(email, password):
    if not email_check(email):
        raise InputError
    if not email_dupe_check(email):
        raise InputError
    if not password_check(password):
        raise InputError

    user = password_check(password)
    token = login(user)
    data = get_user_store()
    for i in data['users']:
        if i['u_id'] == user['u_id']:
            i['token'] = token
    return {
        "u_id": user["u_id"],
        "token": token
    }

#while user_handle is in system already:
#Userhandle = userhandel append 1
#and then you just keep looping until its not there anymore

