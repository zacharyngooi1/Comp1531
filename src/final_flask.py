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
from db import get_messages_store
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
import datetime
from datetime import timezone
#input_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
#chan_id = channels_create(input_dict['token'], 'Hayden', True)

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.debug = True
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
        raise InputError(description="Email not found")
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
    profile = user_profile(token, u_id)
    print(profile)
    return dumps({
        profile
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

@APP.route("/channel/join", methods=["POST"])
def c_join(): 
    #Request information 

    data = request.get_json()

    channel_id = int(data["channel_id"])
    token = data["token"]

    if channel_check(channel_id) == None:
        raise InputError

    if (check_if_channel_is_public(channel_id) == True and 
    check_if_user_in_channel_owner(token, channel_id) == False):
        raise AccessError

    channel_join(token, channel_id)
    return dumps({})

@APP.route("/channels/create", methods=["POST"])
def c_create():
    
    data = request.get_json()

    token = data['token']
    name = data['name']
    is_public = bool(data['is_public'])

    channel_id = channels_create(token, name, is_public)
    print(get_channel_store())
    #message_id = {'message_id':1}
    return dumps(channel_id)
    #return 1

@APP.route("/channel/invite", methods=["POST"])
def c_invite():
    
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

<<<<<<< HEAD
new_user = auth_register("kellykajdf@hdfa.com", "Kejgkjs", "kelly", "wolfe")
new_chl = channels_create(new_user['token'], "name", True)

#APP route
@APP.route("/channel/invite", methods=["POST"])
def c_invite(): 
    # Request information
    #data = request.get_json()

    token = new_user['token']
    u_id = new_user['u_id']

    # Validate token first
    if u_id_check(u_id) == False:
        raise InputError

    channel_id = new_chl['channel_id']
    if channel_check(channel_id) == False: 
        raise InputError

    if check_if_user_in_channel_member(token,channel_id) == True: 
        raise AccessError
    
    channel_invite(token, channel_id, u_id)
    return dumps({})

#APP route
@APP.route("/channel/details/token=new_user['token']&channel_id=new_chl['channel_id']", methods=["GET"])
def c_details(): 
    # Request information
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))


    if channel_check(channel_id) == False: 
        raise InputError

    if check_if_user_in_channel_member(token,channel_id) == True: 
        raise AccessError

    details_channel = channel_details(token, channel_id)
    return dumps({details_channel})

#APP route
@APP.route("/channel/messages", methods=["GET"])
def c_messages(): 
    #Request information 
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")
    start = request.args.get("start")

    if channel_check(channel_id) == None:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    message_dict = channel_messages(token, channel_id, start)
    return dumps({message_dict})

#APP route
@APP.route("/channel/leave", methods=["POST"])
def c_leave(): 
    #Request information 
    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']

    #channel_id = new_chl['channel_id']
    #token = new_user['token']

    if channel_check(channel_id) == None:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    channel_leave(token, channel_id)
    return dumps({})

#APP route
@APP.route("/channel/join", methods=["POST"])
def c_join(): 
    #Request information 

    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']

    if channel_check(channel_id) == None:
        raise InputError

    if (check_if_channel_is_public(channel_id) == True and 
    check_if_user_in_channel_owner(token, channel_id) == False):
        raise AccessError

    channel_join(token, channel_id)
    return dumps({})

#APP route
@APP.route("/channel/addowner", methods=["POST"])
def c_add_owner():
    #Request information 
    data = request.get_json()

    token = data['token']
    u_id = data['u_id']
    channel_id = data['channel_id']

    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == True:
        raise InputError

    if check_if_user_in_channel_owner(token, channel_id) == False:
        raise AccessError

    channel_addowner(token, channel_id, u_id)
    return dumps({})

#APP route
@APP.route("/channel/removeowner", methods=["POST"])
def c_remove_owner():
    #Request information 
    data = request.get_json()

    token = data['token']
    u_id = data['u_id']
    channel_id = data['channel_id']

    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner(token, channel_id) == False:
        raise AccessError

    channel_removeowner(token, channel_id, u_id)
    return dumps({})

#APP route
@APP.route("/channels/list", methods=["GET"])
def c_list(): 
    #Request information 
    token = request.args.get("token")

    if token_check(token) == False:
        raise InputError

    channel_list = channel_list(token)
    return dumps({channel_list})

#APP route
@APP.route("/channels/listall", methods=["GET"])
def c_list_all(): 
    #Request information 
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")

    if token_check(token) == False:
        raise InputError

    channel_list_all = channel_list_all(token)
    return dumps({channel_list_all})
=======
    out = channel_invite(token, channel_id, u_id)
    return dumps(out)
    #return 1

@APP.route("/channel/addowner", methods=["POST"])
def c_addowner():
    
    data = request.get_json()
>>>>>>> c8c95b55506c27ce47e89488650615f605d843e3

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    out = channel_addowner(token, channel_id, u_id)
    
    return dumps(out)
    #return 1

@APP.route("/channel/removeowner", methods=["POST"])
def c_removeowner():
    
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    out = channel_removeowner(token, channel_id, u_id)
    
    return dumps(out)
    #return 1

@APP.route("/channel/details", methods=["GET"])
def c_details():
    
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    print(token)
    return_dict = channel_details(token, channel_id)
    print(return_dict)
    return dumps(return_dict)
    #return 1

@APP.route("/channel/list", methods=["GET"])
def c_list():
    
    token = request.args.get('token')
    return_dict = channel_list(token)
    print(return_dict)
    return dumps(return_dict)
    #return 1

@APP.route("/channels/list_all", methods=["GET"])
def c_listall():
    
    token = request.args.get('token')
    return_dict = channels_list_all(token)
    print(return_dict)
    return dumps(return_dict)
    #return 1

@APP.route("/channel/messages", methods=["GET"])
def c_messages():
    
    #token = request.args.get('token')
    #channel_id = int(request.args.get('channel_id'))
    #start = int(request.args.get('start'))
    token = request.args.get('token')
    ch_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return_dict = channel_messages(token, ch_id,start)
    print(return_dict)
    return dumps(return_dict)
    #return 1


##############################################################
# MESSAGE FLASK FUNCTIONS
##############################################################

@APP.route("/message/send", methods=["POST"])
def send():
    
    data = request.get_json()

    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    message_id = message_send(token, channel_id, message)
    #message_id = {'message_id':1}
    return dumps(message_id)
    #return 1


@APP.route("/message/send_later", methods=["POST"])
def send_later():
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    message = data['message']
    time = int(data['time'])
    message_id = message_send_later(token, channel_id, message,time)
    return dumps(message_id)


@APP.route("/message/react", methods=["POST"])
def react():
    data = request.get_json()

    token = data['token']
    react_id = int(data['react_id'])
    message_id = int(data['message_id'])

    message_react(token,message_id , 1)

    return dumps(message_id)

@APP.route("/message/unreact", methods=["POST"])
def unreact():
    data = request.get_json()

    token = data['token']
    react_id = int(data['react_id'])
    message_id = int(data['message_id'])
    
    message_unreact(token,message_id , 1)
    return dumps(message_id)

#message_pin(hayden_dict['token'], message_id_pin['message_id'])

@APP.route("/message/pin", methods=["POST"])
def pin():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    
    message_pin(token,message_id)
    return dumps(message_id)


@APP.route("/message/unpin", methods=["POST"])
def unpin():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    
    message_unpin(token,message_id)
    return dumps(message_id)



@APP.route("/message/edit", methods=["POST"])
def edit():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']
    
    message_edit(token,message_id,message)
    return dumps(message_id)


@APP.route("/message/remove", methods=["POST"])
def remove():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    
    message_remove(token,message_id)
    return dumps(message_id)




##############################################################
# STANDUP FLASK FUNCTIONS
##############################################################


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
    out = standup_send(token, channel_id, message)   
    return dumps(out)
###############################################################
#DONT TOUCH ANYTHING BELOW THIS LINE OR ZACH WILL BEAT U UP
###############################################################
if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 53250))
