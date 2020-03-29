import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages, channels_create
from db import get_messages_store, get_user_store, get_channel_store, token_check, channel_check, message_check, react_check, get_standup_queue
from message import message_edit, message_remove
from message import message_send, message_send_later,  message_react, message_unreact, message_pin, message_unpin
from standup import standup_start, standup_active, standup_send
from other import search
from auth import auth_register 
from other import users_all
from auth import auth_register
import datetime
from datetime import timezone

hayden_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(hayden_dict['token'], 'Hayden', True)

print(hayden_dict)
print()
print(chan_id)
APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)




@APP.route("/standup/start", methods=['POST'])
def standup_start_flask():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    standup_length = int(data['length'])
    time_finish = standup_start(token, channel_id, standup_length)
    return dumps(time_finish)


@APP.route("/standup/active", methods=['POST'])
def standup_active_flask():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    is_active = standup_active(token, channel_id)
    return dumps(is_active)


@APP.route("/standup/send", methods=['POST'])
def standup_send_flask():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    message = data['message']

    print("Message:",message)
    print("channel_id:",channel_id)
    out = standup_send(token, channel_id, message)
    print(get_standup_queue())
    return dumps(out)

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

