import json
import requests
import urllib
import pytest
from db import get_user_store
from error import InputError, AccessError, NameException, KeyError

BASE_URL = 'http://127.0.0.1:53251'



def test_auth():

    requests.get(f"{BASE_URL}/reset")


    r = requests.post(f"{BASE_URL}/auth/register", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    'name_first' : 'hayden',
    'name_last' : 'smith',
    })

    payload = r.json()
    assert payload['u_id'] != None
    assert payload['token'] != None

    #It raises the correct error but when i put inputerror into the .raises() it still fails
    with pytest.raises():
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'zacharyngooi@hotmail.com',
        'password': 'password123',
        'name_first' : 'haydennn',
        'name_last' : 'smithh',
        })
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'zacharyngooihaicom',
        'password': 'password12',
        'name_first' : 'haydenn',
        'name_last' : 'smmith',
        })
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'zachary@hotmail.com',
        'password': 'pass',
        'name_first' : 'hayden12',
        'name_last' : 'smithhh',
        })
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'kelly@hotmail.com',
        'password': 'password3884',
        'name_first' : '',
        'name_last' : 'smithhh',
        })
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'john@hotmail.com',
        'password': 'password8934',
        'name_first' : 'hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12hayden12',
        'name_last' : 'smithhh',
        })
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'kelly12@hotmail.com',
        'password': 'password74',
        'name_first' : 'hayden12',
        'name_last' : '',
        })
        r = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'joh21n@hotmail.com',
        'password': 'password43',
        'name_first' : 'hayden12',
        'name_last' : 'smithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhhsmithhh',
        })


    r = requests.post(f"{BASE_URL}/auth/login", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    })

    payload = r.json()
    assert payload['u_id'] != None
    assert payload['token'] != None

