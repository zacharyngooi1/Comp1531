from flask import Flask, request 
from json import dumps

APP = Flask(__name__)

data = {
    'user': []
}

def message_send(token, channel_id, message):
    
    return {
        'message_id': 1,
    }

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }

def message_react(token, message_id, react_id):
    return {
    }


#mesage_unreact returns en empty dictionary
#Given a message within a channel the authorised user is part of, remove a "react" to that particular message
def message_unreact(token, message_id, react_id):
    #Checking if the input is valid
    if token is None:
        raise InputError
    if message_id is None:
        raise InputError
    if react_id is None:
        raise InputError
    auth_register()
    auth_login()
    react_id = 0
    return {}

#message_pin returns an empty dictionary
#Given a message within a channel, mark it as "pinned" to be given special display treatment by the frontend
def message_pin(token, message_id):
    return {
    }

def message_unpin(token, message_id):
    return {
    }

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }
