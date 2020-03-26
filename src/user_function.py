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
from db import token_check, channel_check, u_id_check

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))


#liost of channels useeer joined
# list of channels user is owner of 
# list of messages user has done



#APP route
APP.route("workspace/reset", methods=['POST'])
def workspace_reset():
    store = get_user_store()
    pemrission_store = get_permission_store()
    channel_store = get_channel_store
    store = {
        'user': []
    }
    pemrission_store = {}
    return None


@APP.route("/user/profile/sethandle", method=["PUT"])
def user_handle():
        # Request information
        store = get_user_store()
        data = request.get_json()
        token = data['token']
        # Validate token first
        if check_token(token) != 1:
            raise InputError
        # Save input as handle
        set_handle = data['handle_str']
        # Check requirements for length
        if (len(set_handle) <= 2 or >= 20):
            raise InputError
        # Check requirements for duplication
        if check_handle(store,set_handle) == 1:
            raise InputError
        # Change handle to provided handle
        store['token']['handle_str'] = set_handle
        return dumps({})
        
@APP.route("users/all", method=["GET"])
def get_all():
    # Get current data inside store
    store = get_user_store()
    data = request.get_json()
    token = data['token']
    # Authenticate if token is a valid token
    if check_token(store, token) != 1:
        print("Sorry you are not authorized to access this information")
        return None
    return dumps({'Users': store})
    


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
    

# Functions to check errors.
def check_handle(USERDATASTORE , str given_handle):
    for x in USERDATASTORE['user']['handle_string']:
        if x == given_handle:
            return 1
        else:
            return None

def check_token(USERDATASTORE, str given_token):
    for x in USERDATASTORE['user']['token']:
        if x == given_token:
            return 1
        else:
            return None

def check_id(USERDATASTORE, str given_u_id):
    for x in USERDATASTORE['user']['u_id']:
        if x == given_u_id:
            return 1
        else:
            return None

# I have no idea what its supposed to look like
def check_permission(PERMISSIONSTORE, str given_permission_id):
    for x in PERMISSIONSTORE['permission_id']:
        if x == given_permission_id:
            return 1
        else:
            return None

# Check for the channels that the user is authorised in.
# Check how to do this function 
def check_channel(token, channel_id):
    store = get_user_store()
    if 

@APP.route("/search", method=["GET"])
def search():
    store = get_user_store()
    data = request.get_json()
    token = data['token']
    # Authenticate if token is a valid token
    if check_token(store, token) != 1:
        print("Sorry you are not authorized to access this information")
        return None
    query_string = data['string']
    start = data['start']
    channel_id = data['channel_id']
    list = #function im calling e.g get messages form channel
    for message in list['messages']['message']
