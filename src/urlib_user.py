import json
import requests
import urllib
import pytest
from db import get_user_store, get_messages_store, get_channel_store
from error import AccessError, NameException, KeyError
from werkzeug.exceptions import BadRequest, HTTPException
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning) 

BASE_URL = 'http://127.0.0.1:53255'

    
def test_user_profile():

    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    'name_first' : 'bracket',
    'name_last' : 'smith',
    })

    payload = r.json()


############################################################
    #storing data
    test_token = payload['token']
    test_uid = payload['u_id']
    print(test_token)
    print(test_uid)

#########################################################

    query = urllib.parse.urlencode({
        'token': test_token,
        'u_id': test_uid,
    })
    
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query}"))

   # requests.get('URL/user/profile', params=query).json()
    

    print(payload)
    assert payload == {
    'user':{
    'u_id' : test_uid,
    'email': 'zacharyngooi@hotmail.com',
    'name_first': 'bracket',
    'name_last': 'smith',
    'handle_str':'bsmith',
    }
    }


