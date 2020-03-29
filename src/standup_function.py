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

hayden_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(hayden_dict['token'], 'Hayden', True)

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)



@APP.route("/standup/start", methods=["POST"])
def s_start():
    
    data = request.get_json()

    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    message_id = message_send(token, channel_id, message)
    #message_id = {'message_id':1}
    return dumps(message_id)
    #return 1



if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

