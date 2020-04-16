import re
from error import InputError
from db import login, make_user, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from PIL import Image
from db import token_check, channel_check, u_id_check, email_check, email_dupe_check, handle_check
import urllib.request 
import io 

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
        'u_id': user['u_id'],
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']
        }
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
    print(email)
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

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    #need to complete checks 

    # use library to uplpad photo and crop it 
    # save that new photo to server and get new link 
    # that is the link you want to upload to user profile 

    #opens image 
    fd = urllib.request.urlopen(img_url)
    image_file = io.BytesIO(fd.read())
    img = Image.open(image_file)

    #gets current dimensions of picture 
    width, height = img.size

    if img.format != 'JPEG': 
        raise InputError

    #if x_end - x_start > int(width) or y_end- y_start > int(height): 
      #  raise InputError
        
    #slightly confused about how to find left, top, right, and bottom- which one they correspond to 
    left = x_start 
    top = y_start #or should this be y_end? 
    right = x_end 
    bottom = y_end

    img_cropped = img.crop((int(left), int(top), int(right), int(bottom)))
    
    user = token_check(token)
    user['profile_img_url'] = img_url
            

