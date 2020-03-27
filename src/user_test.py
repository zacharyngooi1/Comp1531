import pytest
from error import InputError, AccessError
from user import user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile
from other import users_all, search
from message import message_send
from channel import channels_create
import datetime
from auth import auth_register
from db import token_check, email_check, email_dupe_check, get_messages_store
#If its just import user, use user.(function_to_call) when calling each function for testing

#.Raises wil assert if that error appears as assert() cant be used to check for errors

user_token = auth_register('haydenishere@gmail.com', 'this_ispass', 'hayden', 'smith')
hamish = token_check(user_token['token'])
zach_token = auth_register('Zacharyngooi@gmail.com', 'password', 'Zachary', 'Ngooi')
zach = token_check(zach_token['token'])
kelly_token = auth_register('kellywolfe@gmail.com', 'Password', 'Kelly', 'Wolfe')
kelly = token_check(kelly_token['token'])
    
def test_user_setname_invalid_firstname():
    with pytest.raises(InputError):
        user_profile_setname(hamish['token'], "","Smith") # Less than 1 characters
        user_profile_setname(hamish['token'],"smithsmithsmithsmithsmithsmithsmithsmithsmithsmithsmith","Smith") # More than 50 characers
        
def test_user_setname_invalid_lastname():
    with pytest.raises(InputError):        
        user_profile_setname(hamish['token'], "Im_valid","") # Less than 1 characters
        user_profile_setname(hamish['token'], "Im_valid","SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes") # More than 50 characers
        
def test_user_setname_invalid_bothnames():
    with pytest.raises(InputError):        
        user_profile_setname(hamish['token'], "","") # Less than 1 characters for both
        user_profile_setname(hamish['token'], "SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes","SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes") # More than 50 characers for both

def test_user_setname_valid_bothname():
    # Change first and last name
    user_profile_setname(hamish['token'], 'hello', 'stranger')
    assert(hamish['name_first'] == 'hello')
    assert(hamish['name_last'] == 'stranger')

def test_user_setname_invalid_email():
    with pytest.raises(InputError):      
        user_profile_setemail(hamish['token'],"John@hello") # Invalid email 1
        user_profile_setemail(hamish['token'], "Smith.com") # Invalid email 2

    with pytest.raises(InputError): 
        user_profile_setemail(kelly_token['token'],"Zacharyngooi@gmail.com") #Checking for dupes
        
def test_user_setname_valid_email():
    # Save email
    email = hamish['email']
    # Valid email
    user_profile_setemail(hamish['token'], "my.ownsite@ourearth.org")
    assert(hamish['email'] == "my.ownsite@ourearth.org") 
    # Valid email
    user_profile_setemail(hamish['token'], "ankitrai326@gmail.com") 
    assert(hamish['email'] == "ankitrai326@gmail.com")
    user_profile_setemail(hamish['token'], "haydenishere@gmail.com")
    
def test_user_setname_invalid_display():
    with pytest.raises(InputError):     
        user_profile_sethandle(hamish['token'],"") # Invalid display1
        user_profile_sethandle(hamish['token'],"on")  # Invalid display2
        user_profile_sethandle(hamish['token'],"jonathonjonathonjonathonjonathonjonathonjonathon")  # Invalid display3

    # Save handle_str of 1st user
    zach_handle = zach['handle_str']
    # Save handle_str of 2nd user
    kelly_handle = kelly['handle_str']
    # Save token of 2nd user
    kelly_token = kelly['token']
    with pytest.raises(InputError):  
        # Checking for dupes
        user_profile_sethandle(kelly_token, zach_handle)
        
def test_user_setname_valid_display():      
    # Save display
    display = hamish['handle_str']
    # Valid display change
    user_profile_sethandle(hamish['token'],"jacky")
    assert(hamish['handle_str'] == "jacky") 
     
def test_users_all():
    assert(users_all(hamish['token']) == { 
        'users': [ 

    user_profile(hamish['token'], hamish['u_id']), 

    user_profile(zach['token'], zach['u_id']),

    user_profile(kelly['token'], kelly['u_id']),

       ]   }) # Valid Display

def test_search_valid():
    ch_id = channels_create(hamish['token'], 'comp', True)
    # Send a message
    new_message_id = message_send(hamish['token'], ch_id['channel_id'], 'yes')
    # Save the time created
    message_store = get_messages_store()
    for x in message_store['Messages']:
        if x['message_id'] == new_message_id['message_id']:
            time_created = x['time_created']
    assert(search(hamish['token'], 'yes') == {
       'messages':
        [
            {
                'message_id': new_message_id['message_id'],
                'u_id': hamish['u_id'],
                'message': 'yes',
                'time_created': time_created,
            }
        ]
        
    
        }
        
        ) # Valid Display 

# The following part was done by Mufeed Oomatia
def test_user_profile():

    assert user_profile(12345, 1) ==  {'u_id': 1,'email': 'cs1531@cse.unsw.edu.au','name_first': 'Hayden','name_last': 'Jacobs', 'handle_str': 'hjacobs'}

    assert user_profile(hamish['token'], hamish['u_id']) ==  {
    'u_id': hamish['u_id'],
    'email': hamish['email'],
    'name_first': hamish['name_first'],
    'name_last': hamish['name_last'], 
   	'handle_str': hamish['handle_str']}

   
def test_user_profile():
    with pytest.raises(InputError) as e:
        assert user_profile(12345, "") 
        assert user_profile("", 1) 
        assert user_profile("", "") 
