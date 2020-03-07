import pytest
from error import InputError
from user import user_profile_setname, user_profile_setemail, user_profile_sethandle, email_check, handle_check, user_profile
from other import users_all, search
#If its just import user, use user.(function_to_call) when calling each function for testing

#.Raises wil assert if that error appears as assert() cant be used to check for errors

def test_user_setname_invalid_firstname():
    with pytest.raises(NameError):        
        user_profile_setname("908590435", "","Smith") #Less than 1 characters
        user_profile_setname("908590435","smithsmithsmithsmithsmithsmithsmithsmithsmithsmithsmith","Smith") #More than 50 characers
        
def test_user_setname_invalid_lastname():
    with pytest.raises(NameError):        
        user_profile_setname("908590435", "Im_valid","") #'Less than 1 characters'
        user_profile_setname("908590435", "Im_valid","SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes") #More than 50 characers
        
def test_user_setname_invalid_bothnames():
    with pytest.raises(NameError):        
        user_profile_setname("908590435", "","") #Less than 1 characters for both
        user_profile_setname("908590435", "SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes","SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes") #More than 50 characers for both
        user_profile_setname('908590435',hello,hek)#Check for wrong input
        
def test_user_setname_invalid_email():
    with pytest.raises(NameError):        
        user_profile_setemail("908590435","John@hello") #Invalid email 1
        user_profile_setemail("908590435","Smith.com") #Invalid email 2
        user_profile_setemail("908590435","1") #Checking for dupes
        user_profile_setemail('908590435',3)#Check for wrong input
        
def test_user_setname_valid_email():
    assert(user_profile_setemail("908590435", "my.ownsite@ourearth.org") == "Valid") #Valid email
    assert(user_profile_setemail("908590435", "ankitrai326@gmail.com") == "Valid") #Valid email
    
def test_user_setname_invalid_display():
    with pytest.raises(NameError):     
        user_profile_sethandle("908590435","") #Invalid display1
        user_profile_sethandle("908590435","on")  #Invalid display2
        user_profile_sethandle("908590435","jonathonjonathonjonathonjonathonjonathonjonathon")  #Invalid display3
        user_profile_sethandle("908590435","1") #Checking for dupes
        user_profile_sethandle('908590435',5)#Check for wrong input
        
def test_user_setname_valid_display():      
    assert(user_profile_sethandle("908590435","hello") == 'Valid') #Valid display
     
def test_users_all_invalid():
    with pytest.raises(NameError):
        users_all(this_is_wrong_input) #Check for no inputs
     
def test_users_all():      
    assert(users_all("908590435") ==  {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        }, {
        	'u_id': 2,
        	'email': 'zachary@cse.unsw.edu.au',
        	'name_first': 'Zach',
        	'name_last': 'Ngooi',
        	'handle_str': 'NZach',
        }) #Valid Display
        
def test_search_invalid():
    with pytest.raises(NameError):
        search('908590435',frtg) #Check for invalid input

def test_search_valid(): 
    assert(search("908590435",'this_is_input') == 
        [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],)

#Assumptions:
#Assume token is valid
#Assume correct number of inputs
#Assume only condition is the length of the names
#Assume conditions for correct inputs is set in functions already
#Assume InputError is already implemented

# The following part was done by Mufeed Oomatia
def test_user_profile():
    assert user_profile(12345, 1) ==  {'u_id': 1,'email': 'cs1531@cse.unsw.edu.au','name_first': 'Hayden','name_last': 'Jacobs', 	'handle_str': 'hjacobs'}
   
def test_user_profile():
    with pytest.raises(InputError) as e:
        #assert channels.channels_create() HOW DO I TEST THE INPUT VARIABLE??
        assert user_profile(12345, 2) #technically u_id can be anything but 1
