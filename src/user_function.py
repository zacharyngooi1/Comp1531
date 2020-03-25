import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages
from other import search

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

USERDATASTORE = [
    'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs'
        },
        ]

#IDK what it looks like
PERMISSIONSTORE = {}

def get_permission_store():
    global PERMISSIONSTORE
    return PERMISSIONSTORE

def get_user_store():
    global USERDATASTORE
    return USERDATASTORE

#APP route
def workspace_reset(email, password, name_first, name_last):
    store = get_user_store()
    pemrission_store = get_permission_store
    store = []
    pemrission_store = {}
    return None


# Zach user set handle
# what do i use as the stucture for the glocal store for user such that i can check if its the right user and change the other variables. which variables
# are there supposed to be in the user store?????
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
    
@APP.route("/search", method=["GET"])
def search():
    store = get_user_store()
    data = request.get_json()
    token = data['token']
    # Authenticate if token is a valid token
    if check_token(store, token) != 1:
        print("Sorry you are not authorized to access this information")
        return None
    string = data['string']
    

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
def check_channel(CHANNELDATASTORE, MESSAGESTORE):
