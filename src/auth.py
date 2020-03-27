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
    
def auth_login(email,password):
    if email_check(email) == False:
        raise InputError
    if email_dupe_check(email) == False:
        raise InputError
    if password_check(password) == False:
        raise InputError

    user = password_check(password)
    token = login(user)
    return {
        "u_id": user["u_id"],
        "token": token
    }

#while user_handle is in system already:
#Userhandle = userhandel append 1
#and then you just keep looping until its not there anymore

#@APP.route('/login', methods=['PUT'])
def auth_login(username , password):
    data = getData()
    for user in data['user']:
        if user['username'] == username and user['password'] == hashPassword(password):
            user['token'] = generateToken(username)
            return sendSuccess({
                'token': user['token'],
                'i_id' : user['u_id'],
            })
    return sendError('Username or password incorrect')    


#print(auth_register('hayden@gmail', 'password', 'name_first', 'name_last'))

input_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(input_dict['token'], 'Hayden', True)

rob_dict = auth_register("rob@gmail.com", "paswword123", "Rob", "Ever")

channel_invite(rob_dict['token'], chan_id["channel_id"], rob_dict["u_id"])

message_id = message_send(input_dict['token'], chan_id['channel_id'], "Haydens Message")

message_id2 = message_send(rob_dict['token'], chan_id['channel_id'], "Robs message")
#print("this is user------>",get_user_store())

#message_send_later(input_dict['token'], chan_id['channel_id'], "like uuu", datetime(2020,3,27,14,43,0,0))
#print(get_messages_store())

message_react(input_dict['token'], message_id , 1) 
#print(get_messages_store())
print("  ")
message_unreact(input_dict['token'], message_id , 1) 
#print(get_messages_store())

print("  ")
print("  ")

message_pin(input_dict['token'], message_id)
#print(get_messages_store())

print("  ")
print("  ")
message_unpin(input_dict['token'], message_id)
print(get_messages_store())
print("edit")
message_edit(rob_dict['token'], message_id,'rob editing robs message')
print(get_messages_store())
#rob_dict = auth_register("rob@gmail.com", "paswword123", "Rob", "Ever")
#chan2_id = channels_create(input_dict['token'], 'Someone', True)

#print(channel_details(input_dict['token'], chan_id['channel_id']))
#print("   ")

#channel_invite(rob_dict['token'], chan_id["channel_id"], rob_dict["u_id"])

#print(channel_details(input_dict['token'], chan_id['channel_id']))
#print("   ")

#channel_addowner(input_dict["token"], chan_id["channel_id"], rob_dict["u_id"])
#print(channel_details(input_dict['token'], chan_id['channel_id']))

#print("   ")
#channel_leave(rob_dict['token'], chan_id['channel_id'])
#print(channel_details(input_dict['token'], chan_id['channel_id']))

#print("   ")
#channel_join(rob_dict["token"], chan_id["channel_id"])
#print(channel_details(input_dict['token'], chan_id['channel_id']))

#print("   ")
#channel_removeowner(input_dict["token"], chan_id["channel_id"], rob_dict["u_id"])
#print(channel_details(input_dict['token'], chan_id['channel_id']))

#print("")
#print(chan_id)
#print("")
#print(chan2_id)


