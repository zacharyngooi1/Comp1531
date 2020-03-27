import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from db import get_channel_store, get_messages_store
from db import get_user_store, get_permission_store

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)



#APP route
@APP.route("workspace/reset", methods=['POST'])
def workspace_reset():
    store = get_user_store()
    pemrission_store = get_permission_store()
    channel_store = get_channel_store()
    message_store = get_messages_store()
    store = {
        'users': []
    }
    channel_store = {
        'Channels':[]
    }
    message_store = {
        'Messages': []
    }
    pemrission_store = {}
    return None


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


