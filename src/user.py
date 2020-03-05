import re

def user_profile(token, u_id):
    return {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs'
        },
    }

def user_profile_setname(token, name_first, name_last):
    if (type(name_first) != str or type(name_last) != str):
        raise NameError    
    if (len(name_first) <= 0 or len(name_first) > 50):
        raise NameError
    if (len(name_last) <= 0 or len(name_last) > 50):
        raise NameError
    return {
    }

def email_check(email):
    if (email == 1):
        return 1
    else:
        pass
    
def user_profile_setemail(token, email):
    if (type(email) != str):
        raise NameError    
    checker = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (email_check(email) == 1):
        raise NameError   
    if (re.search(checker, email)) :
        return("Valid")
    else:
        raise NameError
    return {
    }

def handle_check(handle):
    if (handle ==  1):
        return 1
    else:
        pass

def user_profile_sethandle(token, handle_str):
    if (type(handle_str) != str):
        raise NameError 
    if (handle_check(handle_str) == 1):
        raise NameError   
    if (len(handle_str) < 3 or len(handle_str) > 20):   
        raise NameError
    else:
        return("Valid")
    return {
    }
