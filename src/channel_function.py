import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages, channel_invite, channel_details, channel_messages, channel_list, channels_list_all, check_if_user_in_channel_member, check_if_channel_is_public
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner, check_if_user_in_channel_owner, check_if_user_in_channel_owner_uid
from other import search
from db import login, make_user, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from db import token_check, channel_check, u_id_check, handle_check, email_check, email_dupe_check
from other import users_all

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


#APP route
@APP.route("/channel/invite", methods=["POST"])
def c_invite(): 
    # Request information
    data = request.get_json()

    token = data['token']
    u_id = data['u_id']

    # Validate token first
    if u_id_check(u_id) == False:
        raise InputError

    channel_id = data['channel_id']
    if channel_check(channel_id) == False: 
        raise InputError

    if check_if_user_in_channel_member(token,channel_id) == True: 
        raise AccessError
    
    channel_invite(token, channel_id, u_id)
    return dumps({})
'''
#APP route
@APP.route("/channel/details", methods=["GET"])
def c_details(): 
    # Request information
    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']
    if channel_check(channel_id) == False: 
        raise InputError

    if check_if_user_in_channel_member(token,channel_id) == True: 
        raise AccessError

    details_channel = channel_details(token, channel_id)
    return dumps({details_channel})

#APP route
@APP.route("/channel/messages", methods=["GET"])
def c_messages(): 
    #Request information 
    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']
    start = data['start']

    if channel_check(channel_id) == None:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    message_dict = channel_messages(token, channel_id, start)
    return dumps({message_dict})

#APP route
@APP.route("/channel/leave", methods=["POST"])
def c_leave(): 
    #Request information 
    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']

    if channel_check(channel_id) == None:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    channel_leave(token, channel_id)
    return dumps({})

#APP route
@APP.route("/channel/join", methods=["POST"])
def c_join(): 
    #Request information 

    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']

    if channel_check(channel_id) == None:
        raise InputError

    if (check_if_channel_is_public(channel_id) == True and 
    check_if_user_in_channel_owner(token, channel_id) == False):
        raise AccessError

    channel_join(token, channel_id)
    return dumps({})

#APP route
@APP.route("/channel/addowner", methods=["POST"])
def c_add_owner():
    #Request information 
    data = request.get_json()

    token = data['token']
    u_id = data['u_id']
    channel_id = data['channel_id']

    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == True:
        raise InputError

    if check_if_user_in_channel_owner(token, channel_id) == False:
        raise AccessError

    channel_addowner(token, channel_id, u_id)
    return dumps({})

#APP route
@APP.route("/channel/removeowner", methods=["POST"])
def c_remove_owner():
    #Request information 
    data = request.get_json()

    token = data['token']
    u_id = data['u_id']
    channel_id = data['channel_id']

    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner(token, channel_id) == False:
        raise AccessError

    channel_removeowner(token, channel_id, u_id)
    return dumps({})

#APP route
@APP.route("/channels/list", methods=["GET"])
def c_list(): 
    #Request information 
    data = request.get_json()

    token = data['token']

    if token_check(token) == False:
        raise InputError

    channel_list = channel_list(token)
    return dumps({channel_list})

#APP route
@APP.route("/channels/listall", methods=["GET"])
def c_list_all(): 
    #Request information 
    data = request.get_json()

    token = data['token']

    if token_check(token) == False:
        raise InputError

    channel_list_all = channel_list_all(token)
    return dumps({channel_list_all})

#APP route
@APP.route("/channels/create", methods=["POST"])
def c_create():
    #Request information 
    data = request.get_json()

    name = data['name']
    token = data['token']
    is_public= data['is_public']

    if len(name) > 20:
        raise InputError

    channels_create(token, name, is_public)
    return dumps({})




    
'''
    
if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
    
    



    