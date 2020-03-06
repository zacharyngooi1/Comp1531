from auth import auth_register, auth_login
import pytest

# This function tests if the register() function works
def test_register():
    auth_register("devanshakala2000@gmail.com", "12345678", "Devansh", "Kala")

def test_register_valid_email():
    