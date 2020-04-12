import jwt
import hashlib
from json import dumps
from flask import Flask, request
from db import get_user_store, add_user, login, make_user,get_channel_store, get_messages_store,randomString
from db import token_check, channel_check, email_check, email_dupe_check, password_check, find_email, find_code
#from channel import channels_create, channel_details, channel_invite, channel_addowner
#from channel import channel_removeowner, channels_list_all, channel_list, channel_leave, channel_join
#from message import message_send, message_send_later, message_react, message_unreact, message_pin, message_unpin
#from message import message_remove, message_edit
from error import InputError, AccessError
from datetime import datetime
import smtplib 


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

def auth_pw_request(email):
    user = find_email(email)
    
    content = randomString() 
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('cs1531Slackr@gmail.com','authReset123')
    mail.sendmail('cs1531Slackr@gmail.com',email,content)
    mail.close
    user['reset'] = content
    print(user)
    return{}

def auth_pw_reset(code, password):
    us = find_code(code)
    print('1')
    if us == False:
        print('in the if statement')
        raise InputError
    print('2')
    if len(password) < 6:
        raise InputError
    print('3')
    us['password'] = password
    print('4')
    del us['reset']
    print(get_user_store())
    print('5')
    return{}
#hayden_dict =  auth_register('moomatia8@gmail.com', 'password', 'hayden', 'smith')
#auth_pw_request('moomatia8@gmail.com')
#print()
#print(get_user_store())
#while user_handle is in system already:
#Userhandle = userhandel append 1
#and then you just keep looping until its not there anymore

