import pytest
from user import user_profile_setname, user_profile_setemail, user_profile_sethandle, email_check, handle_check
from other import users_all, search
from message import message_send
import datetime
from auth import auth_register
#If its just import user, use user.(function_to_call) when calling each function for testing

#.Raises wil assert if that error appears as assert() cant be used to check for errors

#Creates a function to register a new user
def user_register(email, password, name_first, name_last):
	tmp = auth_register(email, password, name_first, name_last)    
	return {
        'u_id': tmp['u_id'],
        'token': tmp['token'],
		'name_first': name_first,
		'name_last': name_last, 
		'email': email,
		'password': password
    }

# Creates dummy user
hamish = user_register('hamish@email.com', 'yes', 'Hamish', 'butt')
    
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
    # Save first name
    first = hamish['name_last']
    # Save last name    
    last = hamish['name_first']
    # Change first and last name
    user_profile_setname(hamish['token'], "hello","stranger")
    assert(hamish['name_first'] == 'hello')
    assert(hamish['name_last'] == 'stranger')
    
def test_user_setname_invalid_email():
    with pytest.raises(InputError):        
        user_profile_setemail(hamish['token'],"John@hello") # Invalid email 1
        user_profile_setemail(hamish['token'],"Smith.com") # Invalid email 2
    # Creates dummy user
    zach = user_register('Zacharyngooi@email.com', 'password', 'Zachary', 'Ngooi')
    # Save email of 1st user
    zach_email = zach['email']
    # Create another user 
    kelly = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
    # Save token of 2nd user
    kelly_token = kelly['token']
    with pytest.raises(InputError): 
        user_profile_setemail(kelly_token,"Zacharyngooi@email.com") #Checking for dupes
        
def test_user_setname_valid_email():
    # Save email
    email = hamish['email']
    # Valid email
    user_profile_setemail(hamish['token'], "my.ownsite@ourearth.org")
    assert(hamish['email'] == "my.ownsite@ourearth.org") 
    # Valid email
    user_profile_setemail(hamish['token'], "ankitrai326@gmail.com") 
    assert(hamish['email'] == "my.ownsite@ourearth.org")
    
def test_user_setname_invalid_display():
    with pytest.raises(InputError):     
        user_profile_sethandle(hamish['token'],"") # Invalid display1
        user_profile_sethandle(hamish['token'],"on")  # Invalid display2
        user_profile_sethandle(hamish['token'],"jonathonjonathonjonathonjonathonjonathonjonathon")  # Invalid display3
    # Creates dummy user
    zach = user_register('Zacharyngooi@email.com', 'password', 'Zachary', 'Ngooi')
    # Save user_id of 1st user
    zach_handle = zach['u_id']
    # Create another user 
    kelly = user_register('kellywolfe@test.com', 'Password', 'Kelly', 'Wolfe')
    # Save user_id of 2nd user
    kelly_handle = kelly['u_id']
    # Save token of 2nd user
    kelly_token = kelly['token']
    with pytest.raises(InputError):  
        # Checking for dupes
        user_profile_sethandle(kelly_token,zach_handle)
        
def test_user_setname_valid_display():      
    # Save display
    display = hamish['u_id']
    # Valid display change
    user_profile_sethandle(hamish['u_id'],"Jacky")
    assert(hamish['u_id'] == "Jacky") 
     
     
def test_users_all():      
    assert(users_all(hamish['token']) ==  {
        	'u_id': hamish['u_id'],
        	'email': hamish['email'],
        	'name_first': hamish['name_first'],
        	'name_last': hamish['name_last'],
        	'handle_str': 'hbutt',
        }) # Valid Display

def test_search_valid(): 
    # Send a message
    new_message = message_send(hamish['token'],'yes')
    # Save the time created
    time = datetime.datetime.now()
    assert(search(hamish['token'],'yes') == 
        [
            {
                'message_id': new_message['message_id'],
                'u_id': hamish['u_id'],
                'message': 'yes',
                'time_created': time,
            }
        ]) # Valid Display 

#Assumptions:
#Assume token is valid
#Assume correct number of inputs and inputs are of proper type
#Assume only condition is the length of the names
#Assume conditions for correct inputs is set in functions already
#Assume InputError is already implemented
