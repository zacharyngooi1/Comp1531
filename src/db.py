import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from server import defaultHandler
from channel import channel_messages
from other import search
from auth import getData


USERDATASTORE = {
    'user': [ {
        'u_id':,
        'email':,
        'name_first':,
        'name_last':,
        'handle_str':,
        }
    ],
    'Channel': [ {
        'Channels_owned':,
        'Channels_a_part_of':,   
        }
    ],
    'Messages':[ {
        'message_id':,
        }
    ],
}

MESSAGESTORE = {
    'messages': [
            {
                'message_id': ,
                'u_id': ,
                'message': ,
                'time_created': , 
            }
        ],
        'start': ,
        'end':,
    }

    
CHANNELSTORE = {
    'name': ,
        'owner_members': [
            {
                'u_id':,
                'name_first':,
                'name_last':,
            }
        ],
        'all_members': [
            {
                'u_id':,
                'name_first':,
                'name_last':,
            }
        ],
}

def get_permission_store():
    global PERMISSIONSTORE
    return PERMISSIONSTORE

def get_user_store():
    global USERDATASTORE
    return USERDATASTORE


