import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages, channel_invite, channel_details, channel_messages
from channel import channel_list, channels_list_all, check_if_user_in_channel_member, check_if_channel_is_public
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner, check_if_user_in_channel_owner, check_if_user_in_channel_owner_uid, channels_create, channel_invite
from auth import auth_register
from other import search
from db import login, make_user, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from db import token_check, channel_check, u_id_check, handle_check, email_check, email_dupe_check
from message import message_send
from other import users_all


input_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
rob_dict =  auth_register('rob@gmail.com', 'robword', 'rob', 'yalater')
channel_id = channels_create(input_dict['token'], "Chan1", True)
message_id = message_send(input_dict['token'], channel_id['channel_id'], "Hey")
message_id1 = message_send(input_dict['token'], channel_id['channel_id'], "wassup")
message_id2 = message_send(input_dict['token'], channel_id['channel_id'], "hru")
message_id3 = message_send(input_dict['token'], channel_id['channel_id'], "hru")
#chan_id = channels_create(input_dict['token'], 'Hayden', True)
print(input_dict)
print()
print(rob_dict)
print()
print()
APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


#APP route

@APP.route("/channels/create", methods=["POST"])
def c_create():
    
    data = request.get_json()

    token = data['token']
    name = data['name']
    is_public = bool(data['is_public'])

    channel_id = channels_create(token, name, is_public)
    print(get_channel_store())
    #message_id = {'message_id':1}
    return dumps(channel_id)
    #return 1

@APP.route("/channel/invite", methods=["POST"])
def c_invite():
    
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    out = channel_invite(token, channel_id, u_id)
    return dumps(out)
    #return 1

@APP.route("/channel/addowner", methods=["POST"])
def c_addowner():
    
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    out = channel_addowner(token, channel_id, u_id)
    
    return dumps(out)
    #return 1

@APP.route("/channel/removeowner", methods=["POST"])
def c_removeowner():
    
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    out = channel_removeowner(token, channel_id, u_id)
    
    return dumps(out)
    #return 1

@APP.route("/channel/details", methods=["GET"])
def c_details():
    
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    print(token)
    return_dict = channel_details(token, channel_id)
    print(return_dict)
    return dumps(return_dict)
    #return 1

@APP.route("/channel/list", methods=["GET"])
def c_list():
    
<<<<<<< HEAD
=======
    token = request.args.get('token')
    return_dict = channel_list(token)
    print(return_dict)
    return dumps(return_dict)
    #return 1

@APP.route("/channels/list_all", methods=["GET"])
def c_listall():
    
    token = request.args.get('token')
    return_dict = channels_list_all(token)
    print(return_dict)
    return dumps(return_dict)
    #return 1

@APP.route("/channel/messages", methods=["GET"])
def c_messages():
    
    #token = request.args.get('token')
    #channel_id = int(request.args.get('channel_id'))
    #start = int(request.args.get('start'))
    token = input_dict['token']
    ch_id = channel_id['channel_id']
    start = 1
    return_dict = channel_messages(token, ch_id,start)
    print(return_dict)
    return dumps(return_dict)
    #return 1


>>>>>>> c8c95b55506c27ce47e89488650615f605d843e3
if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
    
    



