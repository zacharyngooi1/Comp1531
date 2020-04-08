import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import json
import requests
import urllib
import pytest
from db import get_user_store, get_messages_store, get_channel_store
from error import AccessError, NameException, KeyError
from werkzeug.exceptions import BadRequest, HTTPException
from urllib.error import HTTPError


BASE_URL = 'http://127.0.0.1:5324599'

# KISS ME
def set_up_user1_and_reset():

    # Reset workspace
    requests.get(f"{BASE_URL}/reset")
     
    # Create User 
    request_this = requests.post(f"{BASE_URL}/auth/register", json={
    'email': 'zacharyngooi@hotmail.com',
    'password': 'password',
    'name_first' : 'bracket',
    'name_last' : 'smith',
    })

    payload = request_this.json()

    # Return the dictionary containing token and u_id
    return payload
    
    
def set_up_user2():
     
    # Create User 
    request_this2 = requests.post(f"{BASE_URL}/auth/register", json={
    'email': 'Haydensmith@hotmail.com',
    'password': 'password12345',
    'name_first' : 'Hayden',
    'name_last' : 'smith',
    })

    payload2 = request_this2.json()

    # Return the dictionary containing token and u_id
    return payload2


def test_user_profile():

    # Call user set up
    get_user = set_up_user1_and_reset()
    
############################################################
    # Storing data
    test_token = get_user['token']
    test_uid = get_user['u_id']
#########################################################
    # Encode data
    query = urllib.parse.urlencode({
        'token': test_token,
        'u_id': test_uid,
    })
    
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query}"))
    
    # Assert corresponding user profile.
    assert payload == {
    'user':{
    'u_id' : test_uid,
    'email': 'zacharyngooi@hotmail.com',
    'name_first': 'bracket',
    'name_last': 'smith',
    'handle_str':'bsmith',
    }
    }

    # Create another user
    get_user2 = set_up_user2()

############################################################
    # Storing data
    test_token2 = get_user2['token']
    test_uid2 = get_user2['u_id']
#########################################################

    # Create another query
    query2 = urllib.parse.urlencode({
        'token': test_token2,
        'u_id': test_uid2,
    })
    
    # Ask for profile of second user
    payload2 = json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query2}"))
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query}"))
    
    # Assert that both requests get the corresponding user profiles.
    assert payload2 == {
    'user': {
        'u_id' : test_uid2,
        'email': 'Haydensmith@hotmail.com',
        'name_first': 'Hayden',
        'name_last': 'smith',
        'handle_str':'hsmith',
        }
    }
    assert payload == {
    'user': {
        'u_id' : test_uid,
        'email': 'zacharyngooi@hotmail.com',
        'name_first': 'bracket',
        'name_last': 'smith',
        'handle_str':'bsmith',
        }
    }


def test_user_profile_invalid():
    
    # set up user
    get_user = set_up_user1_and_reset()
    
############################################################
    # Storing data
    test_token = get_user['token']
#########################################################

    # Encode query
    query = urllib.parse.urlencode({
        'token': test_token,
        'u_id': 12345,
    })
    query2 = urllib.parse.urlencode({
        'token': test_token,
        'u_id': '34896138746',
    })
    
    # Check for error for invalid user id
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query}")).raise_for_status()
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query2}")).raise_for_status()
        
        
def test_user_set_name():

    # Call user set up
    get_user = set_up_user1_and_reset()
    get_user2 = set_up_user2()
############################################################
    # Storing data
    test_token = get_user['token']
    test_token2 = get_user2['token']
#########################################################
    # Make a request to change the name of the users
    name_change_1 = requests.put(f"{BASE_URL}/user/profile/setname", json={
        'token': test_token,
        'name_first' : 'Jonathan',
        'name_last' : 'Daniels',
    })
    name_change_2 = requests.put(f"{BASE_URL}/user/profile/setname", json={
        'token': test_token2,
        'name_first' : 'Micheal',
        'name_last' : 'Hoffman',
    })

    # Call user database storage
    store = get_user_store()
    
    # Assert that for the correct user, the name has changed
    for user in store['users']:
        if user['token'] == test_token:
            assert user['name_first'] == 'Jonathan'
            assert user['name_last'] == 'Daniels'
            break
            
    for user in store['users']:
        if user['token'] == test_token2:
            assert user['name_first'] == 'Micheal'
            assert user['name_last'] == 'Hoffman'
            
            
def test_user_set_name_invalid():

    # Call user set up
    get_user = set_up_user1_and_reset()
############################################################
    # Storing data
    test_token = get_user['token']
#########################################################
   
   # Assert errors are raised for diff invalid inputs
    with pytest.raises(requests.exceptions.HTTPError):

        name_change = requests.put(f"{BASE_URL}/user/profile/setname", json={
            'token': test_token,
            'name_first' : '',
            'name_last' : 'Daniels',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        name_change = requests.put(f"{BASE_URL}/user/profile/setname", json={
            'token': test_token,
            'name_first' : 'JonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathanJonathan',
            'name_last' : 'Daniels',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        name_change = requests.put(f"{BASE_URL}/user/profile/setname", json={
            'token': test_token,
            'name_first' : 'Jonathan',
            'name_last' : '',
        }).raise_for_status()
    with pytest.raises(requests.exceptions.HTTPError):
        name_change = requests.put(f"{BASE_URL}/user/profile/setname", json={
            'token': test_token,
            'name_first' : 'Jonathan',
            'name_last' : 'DanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDanielsDaniels',
        }).raise_for_status()


def test_user_set_email():

    # Call user set up
    get_user = set_up_user1_and_reset()
    get_user2 = set_up_user2()
############################################################
    # Storing data
    test_token = get_user['token']
    test_token2 = get_user2['token']
#########################################################
    # Make a request to change the email of the users
    email_change_1 = requests.put(f"{BASE_URL}/user/profile/setemail", json={
        'token': test_token,
        'email' : 'Jonathan@hotmail.com',
    })
    email_change_2 = requests.put(f"{BASE_URL}/user/profile/setemail", json={
        'token': test_token2,
        'email' : 'Micheal@gmail.com',
    })

    # Call user database storage
    store = get_user_store()
    
    # Assert that for the correct user, the email has changed
    for user in store['users']:
        if user['token'] == test_token:
            assert user['email'] == 'Jonathan@hotmail.com'
            break
            
    for user in store['users']:
        if user['token'] == test_token2:
            assert user['email'] == 'Micheal@gmail.com'
            



def test_user_set_email_invalid():

    # Call user set up
    get_user = set_up_user1_and_reset()
    get_user2 = set_up_user2()
############################################################
    # Storing data
    test_token = get_user['token']
#########################################################
   
   # Assert errors are raised for diff invalid inputs
    with pytest.raises(requests.exceptions.HTTPError):
       email_change = requests.put(f"{BASE_URL}/user/profile/setemail", json={
        'token': test_token,
        'email' : 'Jonathanhotmail.com',
    }).raise_for_status()
    
    with pytest.raises(requests.exceptions.HTTPError):
       email_change = requests.put(f"{BASE_URL}/user/profile/setemail", json={
        'token': test_token,
        'email' : 'Jonathan@hotmail',
    }).raise_for_status()
    
    with pytest.raises(requests.exceptions.HTTPError):
       email_change = requests.put(f"{BASE_URL}/user/profile/setemail", json={
        'token': test_token,
        'email' : 'Jonathan',
    }).raise_for_status()
    
    # The email below already is taken by another user so should raise an error
    with pytest.raises(requests.exceptions.HTTPError):
       email_change = requests.put(f"{BASE_URL}/user/profile/setemail", json={
        'token': test_token,
        'email' : 'Haydensmith@hotmail.com',
    }).raise_for_status()


def test_user_set_handle():

    # Call user set up
    get_user = set_up_user1_and_reset()
    get_user2 = set_up_user2()
############################################################
    # Storing data
    test_token = get_user['token']
    test_token2 = get_user2['token']
#########################################################
    # Make a request to change the email of the users
    handle_change_1 = requests.put(f"{BASE_URL}/user/profile/sethandle", json={
        'token': test_token,
        'handle_str' : 'Covid',
    })
    handle_change_2 = requests.put(f"{BASE_URL}/user/profile/sethandle", json={
        'token': test_token2,
        'handle_str' : 'Rickroll',
    })

    # Call user database storage
    store = get_user_store()
    
    # Assert that for the correct user, the email has changed
    for user in store['users']:
        if user['token'] == test_token:
            assert user['handle_str'] =='Covid'==handle_change_1['handle_str']
            break
            
    for user in store['users']:
        if user['token'] == test_token2:
            assert user['handle_str']=='Rickroll'==handle_change_2['handle_str']
            
            
def test_user_set_handle_invalid():

    # Call user set up
    get_user = set_up_user1_and_reset()
    get_user2 = set_up_user2()
############################################################
    # Storing data
    test_token = get_user['token']
#########################################################

   # Assert errors are raised for diff invalid inputs
    with pytest.raises(requests.exceptions.HTTPError):
       handle_change = requests.put(f"{BASE_URL}/user/profile/sethandle", json={
        'token': test_token,
        'handle_str':''
    }).raise_for_status()
    
    with pytest.raises(requests.exceptions.HTTPError):
       handle_change = requests.put(f"{BASE_URL}/user/profile/sethandle", json={
        'token': test_token,
        'handle_str':'covidboomerremovercovidboomerremovercovidboomerremovercovidboomerremovercovidboomerremover'
    }).raise_for_status()
    
    # The handle below is used by user 2 already so this should raise an error
    with pytest.raises(requests.exceptions.HTTPError):
       handle_change = requests.put(f"{BASE_URL}/user/profile/sethandle", json={
        'token': test_token,
        'handle_str':'hsmith'
    }).raise_for_status()
    
    
def test_user_all():

    # Call user set up
    get_user = set_up_user1_and_reset()
    get_user2 = set_up_user2()
############################################################
    # Storing data
    test_token = get_user['token']
    test_uid = get_user['u_id']
    test_token2 = get_user2['token']
    test_uid2 = get_user2['u_id']
#########################################################
    
    # Encode data
    query = urllib.parse.urlencode({
        'token': test_token,
    })
    
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/users/all?{query}"))
    
    # Assert corresponding user profile.
    assert payload == {
        'users':[{
        'u_id' : test_uid,
        'email': 'zacharyngooi@hotmail.com',
        'name_first': 'bracket',
        'name_last': 'smith',
        'handle_str':'bsmith',
        },
        {
        'u_id' : test_uid2,
        'email': 'Haydensmith@hotmail.com',
        'name_first': 'Hayden',
        'name_last': 'smith',
        'handle_str':'hsmith',
        }]
    }
    
    query2 = urllib.parse.urlencode({
        'token': test_token2,
    })
    
    payload2 = json.load(urllib.request.urlopen(f"{BASE_URL}/users/all?{query2}"))
    
    assert payload2 == {
        'users':[{
        'u_id' : test_uid,
        'email': 'zacharyngooi@hotmail.com',
        'name_first': 'bracket',
        'name_last': 'smith',
        'handle_str':'bsmith',
        },
        {
        'u_id' : test_uid2,
        'email': 'Haydensmith@hotmail.com',
        'name_first': 'Hayden',
        'name_last': 'smith',
        'handle_str':'hsmith',
        }]
    }
    
    
