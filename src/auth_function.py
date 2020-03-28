import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages
from other import search
from db import login, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user, password_check
from db import token_check, channel_check, u_id_check, handle_check, email_check, email_dupe_check
from other import users_all
from auth import auth_register, auth_login, auth_logout

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
    if not email_check(email):
        raise InputError(description="Email not valid")
    if email_dupe_check(email):
        raise InputError(description="Email already used")
    if len(password) < 6:
        raise InputError(description="Password less than 6 characters")
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="First name is invalid")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Last name is invalid")

    auth = auth_register(email, password, name_first, name_last)
    auth_token = auth['token']
    auth_uid = auth['u_id']
    
    return dumps({
        'token': auth_token,
        'u_id': auth_uid
    })



@APP.route("/auth/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    if not email_check(email):
        raise InputError(description="Email not valid")
    if not email_dupe_check(email):
        raise InputError(description="Email already used")
    if not password_check(password):
        raise InputError(description="Password is wrong")

    login_info = auth_login(email, password)

    new_token = login_info['token']
    u_id = login_info['u_id']

    return dumps({
        "u_id": u_id,
        "token": new_token
    })


@APP.route("/auth/logout", methods=["POST"])
def logout_user():
    data = request.get_json()
    token = data["token"]
    result = auth_logout(token)

    return dumps({
        'is_success': result
    })


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 53250))
