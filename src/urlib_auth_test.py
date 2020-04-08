import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import json
import requests
import urllib
import pytest
from db import get_user_store, get_messages_store, get_channel_store
from error import AccessError, NameException, KeyError
from werkzeug.exceptions import BadRequest, HTTPException

BASE_URL = 'http://127.0.0.1:5324599'



def test_auth():

    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    'name_first' : 'hayden',
    'name_last' : 'smith',
    })
    payload = r.json()
    store = get_user_store()
    for x in store['users']:
        if x['email'] == 'zacharyngooi@hotmail.com':
            token = x['token']
            id = x['id']
            assert payload['u_id'] == id
            assert payload['token'] == token
############################################################
    #storing data
    test_token = payload['token']
    test_uid = payload['u_id']
#########################################################
    r = requests.post(f"{BASE_URL}/auth/logout", json={
        'token': test_token
    })
    payload = r.json()
    assert payload['is_success'] == True
##########################################################################
    r = requests.post(f"{BASE_URL}/auth/login", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    })

    payload = r.json()

    store = get_user_store()
    for x in store['users']:
        if x['email'] == 'zacharyngooi@hotmail.com':
            token = x['token']
            assert payload['u_id'] == test_uid
            assert payload['token'] == token
#########################################################

        

def test_auth_invalid():
     
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    'name_first' : 'hayden',
    'name_last' : 'smith',
    })


    #It raises the correct error but when i put inputerror into the .raises() it still fails
    with pytest.raises(requests.exceptions.HTTPError):

        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'zacharyngooi@hotmail.com',
        'password': 'password123',
        'name_first' : 'haydennn',
        'name_last' : 'smithh',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'zacharyngooihaicom',
        'password': 'password12',
        'name_first' : 'haydenn',
        'name_last' : 'smmith',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'zachary@hotmail.com',
        'password': 'pass',
        'name_first' : 'hayden12',
        'name_last' : 'smithhh',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'kelly@hotmail.com',
        'password': 'password3884',
        'name_first' : '',
        'name_last' : 'smithhh',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'john@hotmail.com',
        'password': 'password8934',
        'name_first' : 'hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12',
        'name_last' : 'smithhh',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'kelly12@hotmail.com',
        'password': 'password74',
        'name_first' : 'hayden12',
        'name_last' : '',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'joh21n@hotmail.com',
        'password': 'password43',
        'name_first' : 'hayden12',
        'name_last' : 'smithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhh',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/login", json={
        'email': 'zachngooiotmail.com',
        'password': 'password',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/login", json={
        'email': 'kelly@hotmail.com',
        'password': 'password',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.post(f"{BASE_URL}/auth/login", json={
        'email': 'zacharyngooi@hotmail.com',
        'password': 'password1234',
        }).raise_for_status()

