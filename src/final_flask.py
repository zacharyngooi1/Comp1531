import sys
from json import dumps
from datetime import timezone, datetime
import threading
import urllib.request
from urllib.error import HTTPError
import io
from PIL import Image
from flask import Flask, request, url_for
from flask_cors import CORS
from error import InputError, AccessError
from server import defaultHandler
from db import login, make_user, get_channel_store, get_messages_store, get_permission_store
from db import get_user_store, add_user, create_handle, message_create_for_standup
from db import token_check, channel_check, u_id_check, email_check, email_dupe_check
from db import handle_check, password_check, message_check, owner_channel_check
from db import member_channel_check, react_check, reset_store
from db import get_messages_store
from db import load_user_store, load_channels_store, load_messages_store
from db import update_users_store, update_channels_store, update_messages_store
from user import user_profile, user_profile_setemail, user_profile_sethandle, user_remove
from user import user_profile_setname, user_profile_uploadphoto
from auth import auth_register, auth_logout, auth_login, auth_pw_request, auth_pw_reset
from other import users_all, search
from standup import standup_start, standup_active, standup_send
from message import message_send, message_send_later, message_react, message_edit
from message import message_unreact, message_pin, message_unpin, message_remove
from channel import channel_invite, channel_details, channel_messages, channel_leave
from channel import channel_join, channel_addowner, channel_removeowner, channels_create
from channel import channels_list_all, channel_list, check_if_user_in_channel_member
from channel import check_if_user_in_channel_owner, check_if_user_in_channel_owner_uid
from channel import check_if_user_in_channel_member_uid, check_if_channel_is_public
from channel import check_if_channel_exists
from hangman import play_hangman
import uuid
import pickle

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.debug = True
APP.register_error_handler(Exception, defaultHandler)

###############################################################
#DONT TOUCH ANYTHING ABOVE THIS LINE OR ZACH TRASHES U
###############################################################

#input_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
#chan_id = channels_create(input_dict['token'], 'Hayden', True)
#mufeed_dict =  auth_register('moomatia8@gmail.com', 'password', 'Mufeed', 'Oomatia')
#rob_dict =  auth_register('rob@gmail.com', 'password', 'Rob', 'skrt')

#hannel_invite(input_dict['token'], chan_id["channel_id"], rob_dict["u_id"])
#channel_invite(input_dict['token'], chan_id["channel_id"], mufeed_dict["u_id"])

#message_id = message_send(input_dict['token'], chan_id['channel_id'], "Haydens Message")
##message_id1 = message_send(mufeed_dict['token'], chan_id['channel_id'], "Mufeed Message")
#message_id2 = message_send(rob_dict['token'], chan_id['channel_id'], "rob Message")

#print(input_dict)
@APP.route("/admin/userpermission/change", methods=["POST"])
def permission_change():
    data = request.get_json()
    print('this is data->', data)

@APP.route("/admin/user/remove", methods=["DELETE"])
def remove_user():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    print(token, u_id)
    user_remove(token, u_id)
    return dumps({})

@APP.route("/reset", methods=["GET"])
def reset():
    """ This is a flask wrapper for the reset function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    reset_store()
    return dumps({})



###############################################################
# AUTH FLASK FUNCTIONS
###############################################################




@APP.route("/auth/register", methods=["POST"])
def register():
    """ This is a flask wrapper for the reset function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
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
    """ This is a flask wrapper for the auth_login function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary containing the user id (u_id)
        and token is returned.
    """
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
    """ This is a flask wrapper for the auth_logout function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary containing a key called is_success,
        which indicates whether logout has been successful
    """
    data = request.get_json()
    token = data["token"]
    result = auth_logout(token)

    return dumps({
        'is_success': result
    })


@APP.route("/auth/passwordreset/request", methods=["POST"])
def auth_request_password():
    data = request.get_json() 
    email = data['email']
    auth_pw_request(email)
    return dumps({})

@APP.route("/auth/passwordreset/reset", methods=["POST"])
def auth_reset_password():
    data = request.get_json()
    code = data['reset_code']
    password = data['new_password']
    auth_pw_reset(code, password)
    return dumps({})


###############################################################
# USER FLASK FUNCTIONS INCLUDING SEARCH
###############################################################

@APP.route("/user/profile", methods=["GET"])
def get_all():
    """ This is a flask wrapper for the user_profile function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary which contains information
        about user_id, email, first name, last name and handle
    """
    # Get current data inside store
    token = request.args.get("token")
    u_id = request.args.get("u_id")

    # Check for valid u_id
    if not u_id_check(u_id):
        raise InputError(description="u_id is not valid")

    profile = user_profile(token, u_id)
    return dumps({
        'user':profile
    })

@APP.route("/user/profile/setname", methods=["PUT"])
def name_set():
    """ This is a flask wrapper for the user_profile_setname function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
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
    """ This is a flask wrapper for the user_profile_setemail function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
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
    """ This is a flask wrapper for the user/profile/sethandle function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """

    data = request.get_json()
    token = data['token']

    set_handle = data['handle_str']

    if not token_check(token):
        raise InputError(description="Invalid token")
    if (len(set_handle) <= 2 or len(set_handle) >= 20):
        raise InputError(description="Invalid handle")
    if handle_check(set_handle):
        raise InputError(description="Handle already in use")

    user_profile_sethandle(token, set_handle)
    return dumps({})

@APP.route("/user/profile/uploadphoto", methods=["POST"])
def uploadphoto(): 
    """ This is a flask wrapper for the user/profile/uploadphoto function

    Parameters:
        No parameters
    
    Returns:
        (dictionary): Empty dictionary
    """
    #request data 
    data = request.get_json()
    #save data  
    token = data['token']
    img_url = data['img_url']
    x_start = data['x_start']
    y_start = data['y_start']
    x_end = data['x_end']
    y_end = data['y_end']

    #opens image 
    fd = urllib.request.urlopen(img_url)
    image_file = io.BytesIO(fd.read())
    try: 
        img = Image.open(image_file)
    except HTTPError as e:
        print('The server could not fulfill request.')
        print('Error code', e.code)
   
    #gets current dimensions of picture 
    width, height = img.size

    if img.format != 'JPEG': 
        raise InputError

    if int(x_end) - int(x_start) > int(width) or int(y_end)- int(y_start) > int(height): 
       raise InputError

    user_profile_uploadphoto(token, img_url, int(x_start), int(y_start), int(x_end), int(y_end))
    return dumps({})

@APP.route("/users/all", methods=["GET"])
def get_all_users():
    """ This is a flask wrapper for the users_all function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary which contains a list of all
        the users and the details that are associated with them
    """
    token = request.args.get("token")
    if not token_check(token):
        raise InputError(description="Invalid_token")
    user_list = users_all(token)
    return dumps({
        'users': user_list['users']
    })



@APP.route("/search", methods=["GET"])
def search_message():
    """ This is a flask wrapper for the search function

    Parameters:
        No parameters

    Returns:
        (dictionary): Creates a dictionary which contains a key called
        messages which resturns a collection of the messages (which match
        a query string) from all of the channels that the user is part of.
        These messages are sorted from most recent to least recent.
    """
    token = request.args.get("token")
    query_str = request.args.get("query_str")
    if not token_check(token):
        raise InputError(description="Invalid_token")
    message_list = search(token, query_str)

    return dumps({
        "messages" : message_list['messages']
    })


###############################################################
# CHANNEL FLASK FUNCTIONS
###############################################################

@APP.route("/channels/create", methods=["POST"])
def c_create():
    """ This is a flask wrapper for the channels_create function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary with the channel_id of the new channel
    """
    data = request.get_json()

    token = data['token']
    name = data['name']
    is_public = bool(data['is_public'])
    channel_id = channels_create(token, name, is_public)

    return dumps(channel_id)

@APP.route("/channel/invite", methods=["POST"])
def c_invite():
    """ This is a flask wrapper for the channel_invite function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    if not channel_check(channel_id):
        raise InputError(description="Invalid channel")

    if check_if_user_in_channel_member_uid(token, channel_id):
        raise AccessError(description="User is not a member in channel")

    out = channel_invite(token, channel_id, u_id)
    return dumps(out)

#APP route
@APP.route("/channel/leave", methods=["POST"])
def c_leave():
    """ This is a flask wrapper for the channel_leave function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """

    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']

    if channel_check(channel_id) is None:
        raise InputError(description="Channel invalid id")
    if not check_if_user_in_channel_member(token, channel_id):
        raise AccessError(description="User not a member of channel")

    channel_leave(token, channel_id)
    return dumps({})

#APP route
@APP.route("/channel/join", methods=["POST"])
def c_join():
    """ This is a flask wrapper for the channel_join function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    data = request.get_json()

    channel_id = data['channel_id']
    token = data['token']

    if channel_check(channel_id) is None:
        raise InputError(description="Wrong channel ID")

    if not check_if_channel_is_public(channel_id):
        raise AccessError(description="Channel is not public")
    if check_if_user_in_channel_member(token, channel_id):
        raise AccessError(description="User already member of channel")

    channel_join(token, channel_id)
    return dumps({})

#APP route
@APP.route("/channel/addowner", methods=["POST"])
def c_add_owner():
    """ This is a flask wrapper for the channel_addowner function

    Parameters:
        No parameters
    
    Returns:
        (dictionary): Empty dictionary
    """
    #Request information
    data = request.get_json()

    token = data['token']
    u_id = data['u_id']
    channel_id = data['channel_id']

    if not channel_check(channel_id):
        raise InputError(description="Channel is invalid")

    if check_if_user_in_channel_owner_uid(u_id, channel_id):
        raise InputError(description="User already owner of channel")

    if check_if_user_in_channel_owner(token, channel_id):
        raise AccessError(description="User already owner of channel")

    channel_addowner(token, channel_id, u_id)
    return dumps({})

@APP.route("/channel/removeowner", methods=["POST"])
def c_removeowner():
    """ This is a flask wrapper for the channel_removeowner function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    if not channel_check(channel_id):
        raise InputError(description="Channel is invalid")
    if not check_if_user_in_channel_owner_uid(u_id, channel_id):
        raise InputError(description="User not owner of channel")
    if not check_if_user_in_channel_owner(token, channel_id):
        raise AccessError(description="User not owner of channel")

    out = channel_removeowner(token, channel_id, u_id)

    return dumps(out)

@APP.route("/channel/details", methods=["GET"])
def c_details():
    """ This is a flask wrapper for the channel_details function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary which contains details about
        the channel(the name of the channel, owners of the channels
        and all the members of the channel)
    """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    if not channel_check(channel_id): 
        raise InputError(description="channel id not found")
    if not check_if_user_in_channel_member(token, channel_id): 
        raise AccessError(description="User in channel members not found")

    return_dict = channel_details(token, channel_id)
    return dumps(return_dict)


@APP.route("/channels/list", methods=["GET"])
def c_list():
    """ This is a flask wrapper for the channel_list function

    Parameters:
        No parameters

    Returns:
        (dictionary): This dictionary contains a list of all the 
        channels that the user is part of and their associated
        details
    """

    token = request.args.get('token')

    if not token_check(token):
        raise AccessError(description="Invalid token")

    return_dict = channel_list(token)
    return dumps(return_dict)


@APP.route("/channels/listall", methods=["GET"])
def c_listall():
    """ This is a flask wrapper for the channels_list_all function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary which contains the key called
        channels and is a list of channels and their associated details
    """

    token = request.args.get('token')

    if not token_check(token):
        raise AccessError(description="Invalid token")

    return_dict = channels_list_all(token)
    return dumps(return_dict)


@APP.route("/channel/messages", methods=["GET"])
def c_messages():
    """ This is a flask wrapper for the channel_messages function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary containing messages which
        are between the start value and the end value. This dictionary
        contains the keys of messages, start and end.
    """

    token = request.args.get('token')
    ch_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    if not channel_check(ch_id):
        raise InputError(description="channel id not found")

    if not check_if_user_in_channel_member(token, ch_id):
        raise AccessError("User not a member of channel")

    return_dict = channel_messages(token, ch_id, start)
    return dumps(return_dict)
    #return 1


##############################################################
# MESSAGE FLASK FUNCTIONS
##############################################################

@APP.route("/message/send", methods=["POST"])
def send():
    """ This is a flask wrapper for the message_send function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary containing the message_id
        of the message that was sent.
    """
    data = request.get_json()

    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    if len(message) >= 1000:
        raise InputError(description="Message is too long")
    if not check_if_user_in_channel_member(token, channel_id):
        raise AccessError(description="User not member of channel")
    message_id = message_send(token, channel_id, message)

    return dumps(message_id)


@APP.route("/message/sendlater", methods=["POST"])
def send_later():
    """ This is a flask wrapper for the message_send_later function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary containing the message_id
        of the message that was sent.
    """
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    message = data['message']
    time = (data['time_sent'])

    if len(message) >= 1000:
        raise InputError(description="Message is too long")
    if not check_if_channel_exists(channel_id):
        raise InputError(description="Channel does not exist")
    if int(time) < int(datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()):
        raise InputError(description="Invalid time")
    if not check_if_user_in_channel_member(token, channel_id):
        raise AccessError(description="User not member of channel")

    message_id = message_send_later(token, channel_id, message, time)
    return dumps(message_id)


@APP.route("/message/react", methods=["POST"])
def react():
    """ This is a flask wrapper for the message_react function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    data = request.get_json()

    token = data['token']
    react_id = int(data['react_id'])
    message_id = int(data['message_id'])

    if react_id != 1:
        raise InputError(description="Invalid react id")
    if not token_check(token):
        raise AccessError(description="Invalid user")
    user = token_check(token)
    if react_check(message_id, user['u_id'], react_id):
        raise InputError(description="Already reacted")

    message_react(token, message_id, 1)

    return dumps({})

@APP.route("/message/unreact", methods=["POST"])
def unreact():
    """ This is a flask wrapper for the message_unreact function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary.
    """
    data = request.get_json()

    token = data['token']
    react_id = int(data['react_id'])
    message_id = int(data['message_id'])

    if react_id != 1:
        raise InputError(description="Invalid react id")
    if not token_check(token):
        raise AccessError(description="Invalid user")
    user = token_check(token)
    if not react_check(message_id, user['u_id'], react_id):
        raise InputError(description="Already reacted")

    message_unreact(token, message_id, 1)
    return dumps({})

#message_pin(hayden_dict['token'], message_id_pin['message_id'])

@APP.route("/message/pin", methods=["POST"])
def pin():
    """ This is a flask wrapper for the message_pin function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])

    if message_check(message_id) is None:
        raise InputError(description="Invalid id")
    message = message_check(message_id)
    if message['is_pinned']:
        raise InputError(description="Already pinned")
    if not check_if_user_in_channel_member(token, message['channel_id']):
        raise AccessError(description="User not member")
    if not check_if_user_in_channel_owner(token, message['channel_id']):
        raise AccessError(description="User not Owner")

    message_pin(token,message_id)
    return dumps(message_id)


@APP.route("/message/unpin", methods=["POST"])
def unpin():
    """ This is a flask wrapper for the message_unpin function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary.
    """
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])

    if message_check(message_id) is None:
        raise InputError(description="Invalid id")
    message = message_check(message_id)
    if not message['is_pinned']:
        raise InputError(description="Already unpinned")
    if not check_if_user_in_channel_member(token, message['channel_id']):
        raise AccessError(description="User not member")
    if not check_if_user_in_channel_owner(token, message['channel_id']):
        raise AccessError(description="User not Owner")

    message_unpin(token, message_id)
    return dumps(message_id)



@APP.route("/message/edit", methods=["PUT"])
def edit():
    """ This is a flask wrapper for the message_edit function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']

    message_probe = message_check(message_id)
    user = token_check(token)

    if not check_if_user_in_channel_owner(token, message['channel_id']):
        raise AccessError(description="User not owner")
    if user['u_id'] != message_probe['user_id']:
        raise AccessError(description="User not sender")

    message_edit(token, message_id, message)
    return dumps(message_id)


@APP.route("/message/remove", methods=["DELETE"])
def remove():
    """ This is a flask wrapper for the message_remove function

    Parameters:
        No parameters

    Returns:
        (dictionary): Empty dictionary
    """
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])

    message_probe = message_check(message_id)
    user = token_check(token)

    if message_probe is None:
        raise InputError(description="Message not found")
    if not check_if_user_in_channel_owner(token, message['channel_id']):
        raise AccessError(description="User not owner")
    if user['u_id'] != message_probe['user_id']:
        raise AccessError(description="User not sender")

    message_remove(token, message_id)
    return dumps(message_id)




##############################################################
# STANDUP FLASK FUNCTIONS
##############################################################


@APP.route("/standup/start", methods=['POST'])
def standup_start_flask():
    """ This is a flask wrapper for the standup_start function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary containing the key named time_finish.
        time_finish refers to the time that the standup finishes.
    """
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    standup_length = int(data['length'])
    required_channel = channel_check(channel_id)
    #if required_channel is None:
    #    raise InputError(description="Wrong channel ID")
    #if required_channel['standup']['time_standup_finished'] != None:
    #    if datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() < required_channel['standup']['time_standup_finished']:
    #        raise InputError(description="There is already a standup running in this channel. Only one standup can run at a time.")
    time_finish = standup_start(token, channel_id, standup_length)
    return dumps(time_finish)


@APP.route("/standup/active", methods=['GET'])
def standup_active_flask():
    """ This is a flask wrapper for the standup_active function

    Parameters:
        No parameters

    Returns:
        (dictionary): A dictionary containing two keys called is_active
        and time_finish. is_active lets the user know if the standup is
        active and time_finish refers to when the standup finishes.
    """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    #if channel_check(channel_id) is None:
    #    raise InputError(description="Wrong channel ID")
    is_active = standup_active(token, channel_id)
    return dumps(is_active)


@APP.route("/standup/send", methods=['POST'])
def standup_send_flask():
    """ This is a flask wrapper for the standup_send function

    Parameters:
        No parameters

    Returns:
        (dictionary):Empty dictionary.
    """
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    message = data['message']
    #if channel_check(channel_id) is None:
    #    raise InputError(description="Wrong channel ID")
    #if len(message) > 1000:
    #    raise InputError(description="Message cannot be more than 1000 characters long")
    #if check_if_user_in_channel_member_uid(token, channel_id):
    #    raise AccessError(description="User is not a member in channel")
    #if standup_active(token,channel_id)['is_active'] == False:
    #    raise InputError(description="There is not a standup going on right now")
    out = standup_send(token, channel_id, message)   
    return dumps(out)



###DO NOT REMOVE THE FOLLOWING FUNCTIONS (OR MOVE TO db.py) BECAUSE THEY ARE ESSENTIAL FOR MAKING STANDUPS AND DATASTORE WORK.
# update message function
# Step 1: Check if standup is running
# Step 2: If running, send the standup message using message_send (time_now >time_sent) 
def update_message():
    channel_store = get_channel_store()
    # The following piece of code does the following:
    # 1. Loop through each of the channels
    # 2. Check if message at the end of statdup is sent
    # 3. If not send the message
    for channel in channel_store['Channels']:
        if (not channel['standup']['is_message_sent']) and (channel['standup']['time_standup_finished'] is not None):
            user = u_id_check(channel['standup']['u_id_standup_started'])
            if (int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) > int(channel['standup']['time_standup_finished'])):
                message_send(user['token'], channel['channel_id'], channel['standup']['standup_message'])
    return

def update_standup():
    channel_store = get_channel_store()
    for channel in channel_store['Channels']:
        if (not channel['standup']['is_message_sent']) and (channel['standup']['time_standup_finished'] is not None):
            if (int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) > int(channel['standup']['time_standup_finished'])):
                channel['standup']['is_standup_active'] = False
                channel['standup']['time_standup_finished'] = None
                channel['standup']['u_id_standup_started'] = 0
                channel['standup']['is_message_sent'] = True
                channel['standup']["standup_message"] = ""
    return

def timer_action():
    timer = threading.Timer(0.5, timer_action)
    timer.start()
    update_message()
    update_standup()



# DONT REMOVE THE FOLLOWING LINE. IT IS IMPORTANT FOR MAKING STANDUPS WORK
timer_action()

def timer_data_store_action():
    timer = threading.Timer(0.5, timer_data_store_action)
    timer.start()
    update_users_store()
    update_channels_store()
    update_messages_store()

# DON'T REMOVE THE FOLLOWING LINE. IT IS IMPORTANT FOR MAKING DATASTORE WORK
load_user_store()
load_channels_store()
load_messages_store()
timer_data_store_action()

###############################################################
#DONT TOUCH ANYTHING BELOW THIS LINE OR ZACH TRASHES U
###############################################################

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 52377), debug = False)
