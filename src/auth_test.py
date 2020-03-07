#By Devansh Kala (Student I.d. - z5161391)
from auth import auth_register, auth_login, auth_logout
import pytest
from error import InputError

"""The following functions test auth_register"""
# This function tests if the register() function works normally
def test_register():
    auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")

# This function tests if the correct email address is provided
def test_register_invalid_email_address():
    with pytest.raises(InputError) as e :
        auth_register("abc.com", "12345678", "Devansh", "Kala")

# This function tests if the email entered for registration already exists.
def test_register_preexisting_email():
	user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
	with pytest.raises(InputError) as e:
		user_2 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")

# This function tests if the password is of the right size
def test_register_small_password():
	with pytest.raises(InputError) as e:
		auth_register("devanshkala2000@gmail.com", "1", "Devansh", "Kala")

# This function tests if the first name is between 1 and 50 characters in length
def test_register_correct_first_name_size():
	with pytest.raises(InputError) as e:
		auth_register("devanshkala2000@gmail.com", "12345678", "D" * 1000, "Kala")

# This function tests if the last name is between 1 and 50 characters in length
def test_register_correct_last_name_size():
	with pytest.raises(InputError) as e:
		auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "K" * 1000)

# This function tests if auth_register returns an output
def test_auth_register_returns_an_output():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	# Checking if the number of outputs returned in the dicitonary are 2.
	assert len(user_1) == 2

# This function tests if auth_register returns an integer for user_id
def test_user_id_is_integer():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	assert type(user_1["u_id"]) == int

# This function tests if auth_register returns a string for token
def test_token_is_string():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	assert isinstance(user_1["token"], str) == True

"""The following functions test auth_login"""
# The following function checks if auth_login functions normally
def test_auth_login():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	user_1_login = auth_login("devanshkala2000@gmail.com", "12345678")
	assert user_1 == user_2

# The following functions checks if auth_login returns an InputError when the Email entered is not valid
def test_auth_login_invalid_email():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	with pytest.raises(InputError):
		user_1_login = auth_login("abc.com", "12345678")

# The following function checks if the auth_login function returns an InputError when the wmail does not belong to the user.
def test_auth_login_wrong_login():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	with pytest.raises(InputError):
		user_1_login = auth_login("notdevanshkala@gmail.com", "12345678")


# The following function checks if the auth_login function returns an InputError when the password is incorrect
def test_auth_login_wrong_password():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	with pytest.raises(InputError):
		user_1_login = auth_login("devanshkala2000@gmail.com", "1")

"""The following function tests auth_logout"""
#The following function tests if auth_logout functions normally
def test_auth_logout():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	#Auth_logout returns a dictionary containing {'is_success': True}
	result_from_auth_logout = auth_logout(user_1["token"])
	assert result_from_auth_logout['is_success'] == True

#The following function tests if the auth_logout does not work when the wrong token is provided
def test_auth_logout_wrong_token():
	user_1 = auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")
	#Auth_logout returns a dictionary containing {'is_success': True}
	result_from_auth_logout = auth_logout("NOTATOKEN")
	assert result_from_auth_logout['is_success'] == True

#Note to self: One assumption is that auth_register automatically logs in a user. Another assumption is that "NOTATOKEN" is not
#a valid name for a token