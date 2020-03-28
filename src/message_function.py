import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages, channels_create
from db import get_messages_store, get_user_store, get_channel_store, token_check, channel_check, message_check, react_check
from message import message_edit, message_remove
from message import message_send, message_send_later,  message_react, message_unreact, message_pin, message_unpin
from other import search
from auth import auth_register 
from other import users_all
from auth import auth_register
import datetime
from datetime import timezone

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)



@APP.route("/message/send", methods=["POST"])
def send():
    
    data = request.get_json()

    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    message_id = message_send(token, channel_id, message)
    #message_id = {'message_id':1}
    return dumps(message_id)
    #return 1


@APP.route("/message/send_later", methods=["POST"])
def send_later():
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    message = data['message']
    time = int(data['time'])
    message_id = message_send_later(token, channel_id, message,time)
    return dumps(message_id)


@APP.route("/message/react", methods=["POST"])
def react():
    data = request.get_json()

    token = data['token']
    react_id = int(data['react_id'])
    message_id = int(data['message_id'])

    message_react(token,message_id , 1)

    return dumps(message_id)


@APP.route("/message/unreact", methods=["POST"])
def unreact():
    data = request.get_json()

    token = data['token']
    react_id = int(data['react_id'])
    message_id = int(data['message_id'])
    
    message_unreact(token,message_id , 1)
    return dumps(message_id)

#message_pin(hayden_dict['token'], message_id_pin['message_id'])

@APP.route("/message/pin", methods=["POST"])
def pin():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    
    message_pin(token,message_id)
    return dumps(message_id)


@APP.route("/message/unpin", methods=["POST"])
def unpin():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    
    message_unpin(token,message_id)
    return dumps(message_id)



@APP.route("/message/edit", methods=["POST"])
def edit():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']
    
    message_edit(token,message_id,message)
    return dumps(message_id)


@APP.route("/message/remove", methods=["POST"])
def remove():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    
    message_remove(token,message_id)
    return dumps(message_id)



if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

