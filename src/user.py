import re

def user_profile(token, u_id):
    return {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        },
    }

def user_profile_setname(token, name_first, name_last):
    if (len(name_first) == 0):
        raise NameError
    if (len(name_last) == 0):
        raise NameError
    return {
    }

def user_profile_setemail(token, email):
    used_email = 0
    if (used_email == 1) :
        raise NameError
        
    check_email = 1
    checker = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(checker, email)) :
        return("Valid")
    else :
        raise NameError
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }
