from auth import auth_register, auth_login
import pytest
from error import InputError

# This function tests if the register() function works normally
def test_register():
    auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")

# This function tests if the correct email address is provided
def test_register_valid_email_incorrect_email_address():
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