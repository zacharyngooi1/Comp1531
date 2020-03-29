import json
import requests
import urllib
import pytest
from db import get_user_store, get_messages_store, get_channel_store
from error import AccessError, NameException, KeyError
from werkzeug.exceptions import BadRequest, HTTPException
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 

BASE_URL = 'http://127.0.0.1:53250'

    
def test_user_profile():

    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    'name_first' : 'hayden',
    'name_last' : 'smith',
    })

    payload = r.json()


############################################################
    #storing data
    test_token = payload['token']
    test_uid = payload['u_id']

    test_first_name = 0
    test_last_name = 0
    test_handle = 0
    test_email = 0
#########################################################

    query = urllib.parse.urlencode({
        'token': test_token,
        'u_id': test_uid,
    })

    r = requests.get(f"{BASE_URL}/user/profile?{query}")

    payload = r.json()
    assert payload['email'] == 'zacharyngooi@hotmail.com'
    #'u_id' : test_uid,
   # 'email': 'zacharyngooi@hotmail.com',
   # 'name_first': 'hayden',
   # 'name_last': 'smith',
    #'handle_str':'hsmith',
  #  }


