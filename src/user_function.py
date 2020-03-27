import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages
from other import search
from db import login, make_user, channel_add_all_members, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from db import token_check, channel_check, u_id_check, handle_check, email_check, email_dupe_check
from other import users_all

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))


#APP route


@APP.route("/user/profile/sethandle", method=["PUT"])
def user_handle():

        # Request information
        data = request.get_json()

        token = data['token']

        # Validate token first
        if token_check(token) == False:
            raise InputError

        # Save input as handle
        set_handle = data['handle_str']

        # Check requirements for length
        if (len(set_handle) <= 2 or len(set_handle) >= 20):
            raise InputError

        # Check requirements for duplication
        if handle_check(set_handle) == True:
            raise InputError

        user = token_check(token)
        # Change handle to provided handle
        user['handle_str'] = set_handle
        return dumps({})
        
@APP.route("users/all", method=["GET"])
def get_all():
    # Get current data inside store
    data = request.get_json()
    token = data['token']
    # Authenticate if token is a valid token
    if token_check(token) == False:
        print("Sorry you are not authorized to access this information")
        return None
    all_users = users_all(token)
    return dumps({all_users})
    
""""
@APP.route("admin/userpermission/change", method=["GET"])
def permission_change():
    store = get_user_store()
    permission_store = get_permission_store()
    data = request.get_json()
    # Save token id
    token = data['token']
    if check_token(store, token) != 1:
        print("Sorry you are not authorized to access this information")
        return None
    # Save user id
    u_id = data['u_id']
    if check_id(store, u_id) != 1:
        raise InputError
    # Save permission id
    permission_id = data['permission_id']
    if check_permission(permission_store, permission_id) != 1:
        raise InputError
    # IDK what permissions look like
    permissions = data['permissions']
    permission_store['permissions'] = permissions
    return dumps({})
""""

@APP.route("/search", method=["GET"])
def search():
    data = request.get_json()
    token = data['token']
    # Authenticate if token is a valid token
    if token_check(token) == False:
        print("Sorry you are not authorized to access this information")
        return None
    query_string = data['query_str']
    message_list = search(token, query_string)
    return dumps({message_list})
