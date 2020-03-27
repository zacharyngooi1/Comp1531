import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages
from other import search
from db import login, make_user, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from db import token_check, channel_check, u_id_check, handle_check, email_check, email_dupe_check
from other import users_all
from auth import auth_register
APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)



@APP.route("/auth/register", methods=["POST"])
def register():

        # Request information
        data = request.get_json()

        email = data["email"]
        password = data["password"]
        name_first = data["name_first"]
        name_last = data["name_last"]
        
        testing = auth_register(email, password, name_first, name_last)
        testing_token = testing['token']
        testing_uid = testing['u_id']
        
        return dumps({
            'token': testing_token,
            'u_id': testing_uid
        })

@APP.route("/auth", methods=["POST"])
def test():
    data = request.get_json()
    name = data["name"]
    neeeem = data['fuck']
    store = get_user_store()
    store['users'].append(name)
    store['users'].append(neeeem)
    return dumps({
        "store": store
        })

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 53200))
