import pytest
from user import user_profile_setname, user_profile_setemail

#'If its just import user, use user.(function_to_call) when calling each function for testing'

#'.Raises wil assert if that error appears as assert() cant be used to check for errors'

def test_user_setname_invalid_firstname():
    with pytest.raises(NameError):        
        user_profile_setname("908590435", "","Smith")
        user_profile_setname("908590435","smithsmithsmithsmithsmithsmithsmithsmithsmithsmithsmith","Smith")
        
def test_user_setname_invalid_lastname():
    with pytest.raises(NameError):        
        user_profile_setname("908590435", "Im_valid","") #'Less than 1 characters'
        user_profile_setname("908590435", "Im_valid","SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes") #'More than 50 characers'
        
def test_user_setname_invalid_bothnames():
    with pytest.raises(NameError):        
        user_profile_setname("908590435", "","") #'Less than 1 characters for both'
        user_profile_setname("908590435", "SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes","SmithlastyesSmithlastyesSmithlastyesSmithlastyesSmithlastyes") #'More than 50 characers for both'
        
def test_user_setname_invalid_email():
    with pytest.raises(NameError):        
        user_profile_setemail("908590435","John@hello")
        user_profile_setemail("908590435","Smith.com")
        
    assert(user_profile_setemail("908590435", "my.ownsite@ourearth.org") == "Valid")
    assert(user_profile_setemail("908590435", "ankitrai326@gmail.com") == "Valid")
    
        

#'Assumptions:'
#'Assume token is valid'
#'Assume correct number of inputs'
#'Assume only condition is the length of the names
#'Assume conditions for correct inputs is set in functions already'
#'Assume InputError is already implemented
