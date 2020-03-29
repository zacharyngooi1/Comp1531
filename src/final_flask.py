import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError, NameException, KeyError
from server import defaultHandler
from db import login, make_user, get_channel_store, get_messages_store, get_permission_store
from db import get_user_store, add_user, create_handle, message_send_for_standup
from db import token_check, channel_check, u_id_check, email_check, email_dupe_check
from db import handle_check, password_check, message_check, owner_channel_check
from db import member_channel_check, react_check, reset_store
from user import user_profile, user_profile_setemail, user_profile_sethandle
from user import user_profile_setname
from auth import auth_register, auth_logout, auth_login
from other import users_all, search
from standup import standup_start, standup_active, standup_send
from message import message_send, message_send_later, message_react, message_edit
from message import message_unreact, message_pin, message_unpin, message_remove
from channel import channel_invite, channel_details, channel_messages, channel_leave
from channel import channel_join, channel_addowner, channel_removeowner, channels_create
from channel import channels_list_all, channel_list, check_if_user_in_channel_member
from channel import check_if_user_in_channel_owner, check_if_user_in_channel_owner_uid
from channel import check_if_user_in_channel_member_uid, check_if_channel_is_public

#input_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
#chan_id = channels_create(input_dict['token'], 'Hayden', True)

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

###############################################################
#DONT TOUCH ANYTHING ABOVE THIS LINE OR ZACH WILL BEAT U UP  
###############################################################


@APP.route("/reset", methods=["GET"])
def reset():
    reset_store()
    return dumps({})
    


###############################################################
# AUTH FLASK FUNCTIONS
###############################################################

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



###############################################################
# USER FLASK FUNCTIONS INCLUDING SEARCH
###############################################################

@APP.route("/user/profile", methods=["GET"])
def get_all():
    # Get current data inside store
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    if not u_id_check(u_id):
        raise InputError(description="wtf")
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
    token = request.args.get("token")
    # Get current data inside store
    if not token_check(token):
        raise InputError(description="Invalid_token")
    user_list = users_all(token)
    return dumps({
        'users': user_list['users']
    })


@APP.route("/search", methods=["GET"])
def search_message():
    token = request.args.get("token")
    query_str = request.args.get("query_str")
    if not token_check(token):
        raise InputError(description="Invalid_token")
    message_list = search(token, query_str)
    return dumps({
        'Messages': message_list['messages']
    })



###############################################################
# CHANNEL FLASK FUNCTIONS
###############################################################
@APP.route("/channels/create", methods=["POST"])
def c_create():
    #Request information 
    data = request.get_json()
    name = data['name']
    token = data['token']
    is_public= True

    if len(name) > 20:
        raise InputError

    channel_id = channels_create(token, name, is_public)
    return dumps(channel_id)








##############################################################
# STANDUP FLASK FUNCTIONS
##############################################################

@APP.route("/standup/start", methods=['POST'])
def standup_start_flask():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    standup_length = data['length']
    time_finish = standup_start(token, channel_id, standup_length)
    return dumps(time_finish)
"""
@APP.route("/standup/active", methods=['GET'])
def standup_active_flask():
    return dumps(standup_active(request.args.get('token'), request.args.get('channel_id')))

@APP.route("/standup/send", methods=['POST'])
def standup_send_flask():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    standup_length = data['length']


    standup_send(token, channel_id, )
"""
###############################################################
#DONT TOUCH ANYTHING BELOW THIS LINE OR ZACH WILL BEAT U UP
###############################################################
if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 53251))