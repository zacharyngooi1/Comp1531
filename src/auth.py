
import jwt
import hashlib
from json import dumps
from flask import Flask, request

APP = Flask(__name__)
        
SECRET = 'YEET'

data = {
    'user': [{
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs'
        },]
}

def getData():
    global data
    return data

def sendSuccess(data):
    return dumps(data)

def sendError(message):
    return dumps({
        '_error' : message,
    })

def generateToken(username):
    global SECRET
    encoded = jwt.encode({'username': username}, SECRET, algorithm='HS256')
    print(encoded)
    return str(encoded)

def getUserFromToken(token):
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decoded['username']

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

#@APP.route('/secrets', methods=['GET'])
def get():
    if getUserFromToken(request.args.get('token')) is None:
        return sendError('Invalid token')
    return sendSuccess({
        'secrets' : ['I', 'like', 'rats'],
    })

#@APP.route('/register', methods=['POST'])
def create():
    data = getData()
    username = request.form.get('username')
    password = request.form.get('password')
    data['users'].append({
        'username': username,
        'password': hashPassword(password),
    })
    print(data)
    return sendSuccess({
        'token': generateToken(username),
    })

#Assumption: Assume there are no users with the same firstname + lastname + first letter of their password
def auth_register(email, password, name_first, name_last):
    return_dict = {}
    u_id = len(data['users']) 
    token =  generateToken(name_first + name_last + password[0])
    return_dict['u_id'] = u_id
    return_dict['token'] = token
    return return_dict

def user_register(email, password, name_first, name_last):
	tmp = auth_register(email, password, name_first, name_last)    
	return {
        'u_id': tmp['u_id'],
        'token': tmp['token'],
		'name_first': name_first,
		'name_last': name_last, 
        'handle_str': (name_first[0]+name_last).lower,
		'email': email,
		'password': password
    }

#@APP.route('/login', methods=['PUT'])
def auth_login(username , password):
    data = getData()
    for user in data['users']:
        if user['username'] == username and user['password'] == hashPassword(password):
            return sendSuccess({
                'token': generateToken(username),
            })
    return sendError('Username or password incorrect')    

#if __name__ == '__main__':
#    APP.run()


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
