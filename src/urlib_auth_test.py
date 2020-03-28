import json
import requests
import urllib
import pytest
from db import get_user_store

BASE_URL = 'http://127.0.0.1:53251'



def test_system():

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


