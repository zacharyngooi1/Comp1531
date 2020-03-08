import pytest
from auth import auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave
from channels import channels_create
from error import InputError, AccessError

"""The following functions test channel_invite"""
#This function tests whether channel_invite works properly
def test_channel_invite():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]
    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]
    #channels_create() creates a new channel and retuns a {channel_id}
    new_channel = channels_create(user_1_token, "CLASSYISASTATEOFTHEMINDCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"] 
    channel_invite(user_1_token, new_channel_channel_id, user_2_u_id)
    #channel_details() returns {name, owner_members, all_members}
    #all_members is a list of dictionaries containing {u_id, name_first, name_last}
    details_of_new_channel = channel_details(user_1_token, new_channel_channel_id)
    # A list with dictionaries each with information about owners (which is u_id, name_first, name_last)
    list_of_members = details_of_new_channel["all_members"]
    valid_user_in_channel = 0
    #Checks if the user has joined the channel
    for member in list_of_members:
        if member["u_id"] == user_2_u_id:
            valid_user_in_channel == 1
    assert valid_user_in_channel == 1

#The following function tests whether channel_invite returns an InputError when the wrong channel_id is provided
def test_channel_invite_wrong_channel_id():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]
    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]
    #channels_create() creates a new channel and retuns a {channel_id}
    new_channel = channels_create(user_1_token, "CLASSYISASTATEOFTHEMINDCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"] 
    with pytest.raises(InputError) as e:
        channel_invite(user_1_token, new_channel_channel_id * 6789, user_2_u_id)

#The following function tests whether channel_invite returns an InputError when the wrong u_id is provided
def test_channel_invite_wrong_user_id():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]
    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]
    #channels_create() creates a new channel and retuns a {channel_id}
    new_channel = channels_create(user_1_token, "CLASSYISASTATEOFTHEMINDCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"] 
    with pytest.raises(InputError) as e:
        channel_invite(user_1_token, new_channel_channel_id, user_2_u_id * 6789)

#The following function tests whether channel_invite returns an AccessError when the authorised user (user_1) is not already a member of the channel
def test_channel_invite_wrong_authorised_user():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]
    
    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]
    
    user_3 = auth_register("johncitizen@gmail.com", "2021222324252627", "John", "Citizen")
    user_3_u_id = user_3["u_id"]
    user_3_token = user_3["token"]
    
    #channels_create() creates a new channel and retuns a {channel_id}
    new_channel = channels_create(user_1_token, "CLASSYISASTATEOFTHEMINDCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"] 
    with pytest.raises(AccessError) as e:
        channel_invite(user_3_token, new_channel_channel_id, user_2_u_id)

"""The following functions test channel_details"""
# Testing if the channel_details function works properly
def test_channel_details():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_user_id = user_1["u_id"]
    user_1_token = user_1["token"]
    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]
    new_channel_details = channel_details(user_1_token, new_channel_channel_id)
    
    assert new_channel_details["name"] == "NEWCHANNEL"
    assert new_channel_details["owner_members"] == {
        'u_id' : user_1_user_id,
        'name_first' : 'Devansh',
        'name_last' : 'Kala',
    }
    assert new_channel_details["all_members"] == {
        'u_id' : user_1_user_id,
        'name_first' : 'Devansh',
        'name_last' : 'Kala',
    }

# Testing if the channel_details function returns an InputError when the channel_id does not refer to a valid channel
def test_channel_details_wrong_channel_id():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_user_id = user_1["u_id"]
    user_1_token = user_1["token"]
    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]
    with pytest.raises(InputError) as e:
        channel_details(user_1_token, new_channel_channel_id * 6789)

#Testing if the channel_details function returns an AccessError when the authorised user is not a member of the channel with channel_id
def test_channel_details_wrong_authorised_user():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]
    
    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]
    
    user_3 = auth_register("johncitizen@gmail.com", "2021222324252627", "John", "Citizen")
    user_3_u_id = user_3["u_id"]
    user_3_token = user_3["token"]
    
    #channels_create() creates a new channel and retuns a {channel_id}
    new_channel = channels_create(user_1_token, "CLASSYISASTATEOFTHEMINDCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"] 
    with pytest.raises(AccessError) as e:
        channel_details(user_3_token, new_channel_channel_id)

"""The following functions test channel_messages"""
#The following function tests whether channel_messages function works normally
def test_channel_messages():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]

    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]

    #channel_message returns a dictionary made of a list of messages (each message is a dictionary) and the start and end of the message
    new_channel_messages = channel_messages(user_1_token, new_channel_channel_id, 0)

#The following function tests whether channel_messages function returns an InputError when the channel_id is not valid
def test_channel_messages_invalid_channel_id():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]

    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]

    #channel_message returns a dictionary made of a list of messages (each message is a dictionary) and the start and end of the message
    with pytest.raises(InputError) as e:
        channel_messages(user_1_token, new_channel_channel_id * 6789, 0)
    
#The following function tests whether channel_messages function returns an InputError when the start is greater than the total number of messages in the channel
def test_channel_messages_start_greater_than_end():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]

    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]

    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]
    #user_2 is added to the channel
    channel_invite(user_1_token, new_channel_channel_id, user_2_u_id)

    #user_1 is used to get the start and end of the messages
    new_channel_channel_messages = channel_messages(user_1_token, new_channel_channel_id, 0)
    new_channel_message_start = new_channel_channel_messages["start"]
    new_channel_message_end = new_channel_channel_messages["end"]

    #user_2 cannot access messages which are greater than the start + end + 1000
    with pytest.raises(InputError) as e:
        channel_messages(user_2_token, new_channel_channel_id, new_channel_message_start + new_channel_message_end + 1000)

#The following function tests whether the channel_messages function returns AccessError when the authorised used is not a member of channel with channel_id
def test_channel_messages_authorised_user_not_member():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]

    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]

    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]

    #user_2 has NOT been added to the channel using channel_invite unlike in the previous function. Hence, an AccessError
    #should be returned when user_2 tries to access the messages.

    #user_2 cannot access messages which are greater than the start + end + 1000
    with pytest.raises(AccessError) as e:
        channel_messages(user_2_token, new_channel_channel_id, 0)

"""The following functions test channel_leave"""
#The following function tests whether the channel_leave function works normally
def test_channel_leave():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_user_id = user_1["u_id"]
    user_1_token = user_1["token"]
    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]
    channel_leave_result = channel_leave(user_1_token, new_channel_channel_id)
    assert channel_leave_result == {}

#The following function tests whether the channel_leave function returns an InputError when channel_id is not a valid channel
def test_channel_leave_wrong_channel_id():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_user_id = user_1["u_id"]
    user_1_token = user_1["token"]
    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]
    with pytest.raises(InputError) as e:
        channel_leave(user_1_token, new_channel_channel_id * 6789)

#The following function tests whether the channel_leave function returns an AccessError when the authorised user is not a member of channel with channel_id
def test_channel_leave_wrong_authorised_user():
    user_1 = auth_register("devanshkala2000@gmail.com", "12345678", "Devansh", "Kala")
    user_1_u_id = user_1["u_id"]
    user_1_token = user_1["token"]
    
    user_2 = auth_register("janesmith@gmail.com", "9101112131414", "Jane", "Smith")
    user_2_u_id = user_2["u_id"]
    user_2_token = user_2["token"]

    new_channel = channels_create(user_1_token, "NEWCHANNEL", True)
    new_channel_channel_id = new_channel["channel_id"]

    with pytest.raises(AccessError) as e:
        channel_leave(user_2_token, new_channel_channel_id)