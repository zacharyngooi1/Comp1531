import re
from error import InputError
from auth import auth_login, auth_register, auth_logout
from db import login, make_user, channel_add_all_members, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from db import token_check, channel_check, u_id_check

def user_profile(token, u_id):

    if token_check(token) == False:
        raise InputError

    # First we need to assert if the u_id is registered
    if u_id_check(u_id) == False:
        raise InputError

    # get required user dict
    user = u_id_check(u_id)
    # create a dict of what we need
    user_prof_dict = {

    }
    user_prof_dict['user_id'] = user['u_id']
    user_prof_dict['email'] = user['email']
    user_prof_dict['first_name'] = user['name_first']
    user_prof_dict['last_name'] = user['name_last']
    user_prof_dict['handle'] = user['handle_str']

    return user_prof_dict

def user_profile_setname(token, name_first, name_last):

    # Check for any name length errors
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError

    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError

    # We need to assert if the token is registered

    if token_check(token) == False:
        raise InputError

    # get required user dict
    user = token_check(token)
    
    user['name_first'] = name_first
    user['name_last'] = name_last

    return {}



def user_profile_setemail(token, email):

      # Check for any name length errors
    if email_check(email) == False:
        raise InputError

    if email_dupe_check(email) == True:
        raise InputError

    # We need to assert if the token is registered

    if token_check(token) == False:
        raise InputError

    # get required user dict
    user = token_check(token)
    user['email'] = email
    
    return {}


def user_profile_sethandle(token, handle_str):

    if len(handle_str) <= 2 or len(handle_str) >= 20:
        raise InputError

    if handle_check(handle_str) == True:
        raise InputError

    # get required user dict
    user = token_check(token)
    user['handle_str'] = handle_str

    return {}



