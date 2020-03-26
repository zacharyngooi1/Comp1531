
import jwt
import hashlib
from json import dumps
from flask import Flask, request
from dp.py import get_permission_store, get_user_store


APP = Flask(__name__)
        
SECRET = 'YEET'


def sendSuccess(data):
    return dumps(data)

def sendError(message):
    return dumps({
        '_error' : message,
    })

def generateToken(username):
    global SECRET
    encoded = jwt.encode({'handle_str': username}, SECRET, algorithm='HS256')
    print(encoded)
    return str(encoded)

def getUserFromToken(token):
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decoded['handle_str']

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


#Assumption: Assume there are no users with the same firstname + lastname + first letter of their password
def auth_register(email, password, name_first, name_last):
    return_dict = {}
    u_id = len(data['user']) 
    token =  generateToken(name_first + name_last + password[0])
    return_dict['u_id'] = u_id
    return_dict['token'] = token
    return_dict['handle_str'] = name_first + name_last #CHANGE THIS LATERR!!!!!!
    return_dict['name_first'] = name_first 
    return_dict['name_last'] = name_last 
    return_dict['email'] = email
    return_dict['password'] = hashPassword(password)
    data['user'].append(return_dict)
    return {'u_id':return_dict['u_id'] , 'token': return_dict['token'], }


def auth_logout(token):
    for user in data['user']:
        if user['token'] == token:
            dummy_value = user.pop('token')
            return True
    return False
    
#while user_handle is in system already:
#Userhandle = userhandel append 1
#and then you just keep looping until its not there anymore

#def user_register(email, password, name_first, name_last):
#	tmp = auth_register(email, password, name_first, name_last)    
#	return {
#        'u_id': tmp['u_id'],
#        'token': tmp['token'],
#		'name_first': name_first,
#		'name_last': name_last, 
 #       'handle_str': (name_first[0]+name_last).lower,
	#	'email': email,
	#	'password': password
    #}

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
