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
from user import user_profile, user_profile_setemail, user_profile_sethandle, user_profile_setname


APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

@APP.route("/user/profile", methods=["GET"])
def get_all():
    # Get current data inside store
    data = request.get_json()
    token = data['token']
    u_id = data['token']
    # Authenticate if token is a valid token
    if not u_id_check(u_id):
        raise InputError
    profile = user_profile(token, u_id)

    return dumps({
        'user': profile
    })

@APP.route("/user/profile/setname", methods=["PUT"])
def name_set():
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']

    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError(description="First name is invalid")
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError(description="Last name is invalid")

    user_profile_setname(token, name_first, name_last)

    return dumps({})

@APP.route("/user/profile/setemail", methods=["PUT"])
def email_set():
    data = request.get_json()
    token = data['token']
    email = data['email']

    if not email_check(email):
        raise InputError(description="Email not valid")
    if email_dupe_check(email):
        raise InputError(description="Email already used")

    user_profile_setemail(token, email)

    return dumps({})


@APP.route("/user/profile/sethandle", methods=["PUT"])
def user_handle():
    # Request information
    data = request.get_json()
    token = data['token']
    # Save input as handle
    set_handle = data['handle_str']
    # Validate token first
    if not token_check(token):
        raise InputError("Invalid token")
    # Check requirements for length
    if (len(set_handle) <= 2 or len(set_handle) >= 20):
        raise InputError(description="Invalid handle")
    # Check requirements for duplication
    if handle_check(set_handle):
        raise InputError(description="Handle already in use")
    user_profile_sethandle(token, set_handle)

    return dumps({})

@APP.route("/users/all", methods=["GET"])
def get_all_users():
    # Get current data inside store
    data = request.get_json()
    token = data['token']
    if not token_check(token):
        raise InputError(description="Invalid_token")
    user_list = users_all(token)
    return dumps({
        'users': user_list['users']
    })


@APP.route("/search", methods=["GET"])
def search_message():
    data = request.get_json()
    token = data['token']
    query_str = data['query_str']
    if not token_check(token):
        raise InputError(description="Invalid_token")
    message_list = search(token, query_str)
    return dumps({
        'Messages': message_list['messages']
    })

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 53250))