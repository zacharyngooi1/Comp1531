import jwt
import hashlib
from json import dumps
from flask import Flask, request
from db import get_user_store, add_user, login, make_user
APP = Flask(__name__)

def sendSuccess(data):
    return dumps(data)

def sendError(message):
    return dumps({
        '_error' : message,
    })

#Assumption: Assume there are no users with the same firstname + lastname + first letter of their password

def auth_register(email, password, name_first, name_last):
    user = add_user(email, password, name_first, name_last)
    token = login(user)
    return {
        "u_id": user["u_id"],
        "token": token
    }

def auth_logout(token):
    for user in data['user']:
        if user['token'] == token:
            dummy_value = user.pop('token')
            return True
    return False
    
#while user_handle is in system already:
#Userhandle = userhandel append 1
#and then you just keep looping until its not there anymore

#@APP.route('/login', methods=['PUT'])
def auth_login(username , password):
    data = getData()
    for user in data['user']:
        if user['username'] == username and user['password'] == hashPassword(password):
            user['token'] = generateToken(username)
            return sendSuccess({
                'token': user['token'],
                'i_id' : user['u_id'],
            })
    return sendError('Username or password incorrect')    


#def auth_login(email, password):
#    return {
#        'u_id': 1,
#        'token': '12345',
#    }

#def auth_logout(token):
#    return {
#        'is_success': True,
#    }

#def auth_register(email, password, name_first, name_last):
#    return {
#        'u_id': 1,
#        'token': '12345',
#    }
