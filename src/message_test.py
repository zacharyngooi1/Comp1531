#import message
#import channels
#import channel
import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channels_create, channel_invite
from message import message_send, message_send_later, message_react, message_unreact, message_pin, message_unpin
from message import message_remove,message_edit
from db import get_messages_store
import datetime
from datetime import timezone
#Assumptions
#All the inputs are valid
hayden_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(hayden_dict['token'], 'Hayden', True)
rob_dict = auth_register("rob@gmail.com", "paswword123", "Rob", "Ever")
#channel_invite(hayden_dict['token'], chan_id["channel_id"], rob_dict["u_id"])

message_id = message_send(hayden_dict['token'], chan_id['channel_id'], "Haydens Message")

def test_message_send():
    assert get_messages_store()['Messages'][0] == {
        'channel_id': chan_id["channel_id"], 
        'message_id': message_id['message_id'], 
        'user_id': hayden_dict['u_id'], 
        'message': 'Haydens Message', 
        'reacts': [], 
        'time_created': get_messages_store()['Messages'][0]['time_created'], 
        'is_pinned': False}

def test_message_send_invalid_InputError():
    with pytest.raises(InputError):
        message_send(hayden_dict['token'], chan_id['channel_id'], "H"*1001)

def test_message_send_invalid_AccessError():
    with pytest.raises(AccessError):
        message_send(rob_dict['token'], chan_id['channel_id'], "Robs message")

message_id1 = message_send_later(hayden_dict['token'], chan_id['channel_id'], "Haydens Message later", (datetime.datetime.now()+  datetime.timedelta(0,1)).replace(tzinfo=timezone.utc).timestamp())


def test_message_send_later():
    assert get_messages_store()['Messages'][1] == {
        'channel_id': chan_id["channel_id"], 
        'message_id': message_id1['message_id'], 
        'user_id': hayden_dict['u_id'], 
        'message': 'Haydens Message later', 
        'reacts': [], 
        'time_created': get_messages_store()['Messages'][1]['time_created'], 
        'is_pinned': False}

def test_message_send_later_invalid_AccessError():
    with pytest.raises(AccessError):
        message_send_later(rob_dict['token'], chan_id['channel_id'], "Robs message",datetime.datetime(2020, 3, 28, 2, 9, 46, 184346).replace(tzinfo=timezone.utc).timestamp())
        
def test_message_send_later_invalid_InputError():
    with pytest.raises(InputError):
        message_send_later(hayden_dict['token'], chan_id['channel_id'], "Hayens message",datetime.datetime(2020, 3, 28, 2, 9, 46, 184346).replace(tzinfo=timezone.utc).timestamp())
print(get_messages_store()['Messages'])


def test_message_react_invalid_InputError1():
    with pytest.raises(InputError):
        message_react(hayden_dict['token'],1 , 1) 

def test_message_react_invalid_InputError2():
    with pytest.raises(InputError):
        message_react(hayden_dict['token'],message_id['message_id'] , 2) 

chan_id_check = channels_create(hayden_dict['token'], 'Hayden', True)
message_id_check = message_send(hayden_dict['token'], chan_id_check['channel_id'], "Haydens Message Check")
message_react(hayden_dict['token'],message_id_check['message_id'] , 1)

def test_message_react():
    assert get_messages_store()['Messages'][2]['reacts'] == [{'u_ids': [hayden_dict['u_id']], 'react_id': 1, 'is_this_user_reacted' : True}] 

def test_message_react_invalid_InputError3():
    with pytest.raises(InputError):
        message_react(hayden_dict['token'],message_id_check['message_id'] , 1)



def test_message_unreact_invalid_InputError1():
    with pytest.raises(InputError):
        message_unreact(hayden_dict['token'],1 , 1) 

def test_message_unreact_invalid_InputError2():
    with pytest.raises(InputError):
        message_unreact(hayden_dict['token'],message_id['message_id'] , 2) 


message_id_unreact = message_send(hayden_dict['token'], chan_id_check['channel_id'], "Haydens Message Check")
message_react(hayden_dict['token'],message_id_unreact['message_id'] , 1)
message_unreact(hayden_dict['token'],message_id_unreact['message_id'] , 1)

def test_message_unreact():
    assert get_messages_store()['Messages'][3]['reacts'] == [] 


def test_message_unreact_invalid_InputError3():
    with pytest.raises(InputError):
        message_unreact(hayden_dict['token'],message_id_unreact['message_id'] , 1)


##test pin

chan_id_pin = channels_create(hayden_dict['token'], 'Pin_check', True)
FOMO_dict = auth_register("Fomo@gmail.com", "oooswword123", "Suss", "picious")
channel_invite(hayden_dict['token'], chan_id_pin["channel_id"], rob_dict["u_id"])

message_id_pin = message_send(hayden_dict['token'], chan_id_pin['channel_id'], "Haydens Message Check")


def test_message_pin_invalid_AccessError1():
    with pytest.raises(AccessError):
        message_pin(rob_dict['token'], message_id_pin['message_id'])

def test_message_pin_invalid_AccessError2():
    with pytest.raises(AccessError):
        message_pin(FOMO_dict['token'], message_id_pin['message_id'])

message_pin(hayden_dict['token'], message_id_pin['message_id'])

def test_message_pin():
    assert get_messages_store()['Messages'][4]['is_pinned'] == True

def test_message_pin_invalid_InputError2():
    with pytest.raises(InputError):
        message_pin(hayden_dict['token'], message_id_pin['message_id'])


#unpin tests

message_id_unpin = message_send(rob_dict['token'], chan_id_pin['channel_id'], "Robs message to be pinned/ unpinned")
message_pin(hayden_dict['token'], message_id_unpin['message_id'])

def test_message_unpin_invalid_InputError1():
    with pytest.raises(InputError):
        message_unpin(rob_dict['token'], message_id_unpin['message_id'])

def test_message_unpin_invalid_AccessError():
    with pytest.raises(AccessError):
        message_unpin(FOMO_dict['token'], message_id_unpin['message_id'])

message_unpin(hayden_dict['token'], message_id_unpin['message_id'])

def test_message_unpin():
    assert get_messages_store()['Messages'][5]['is_pinned'] == False

def test_message_unpin_invalid_InputError2():
    with pytest.raises(InputError):
        message_unpin(hayden_dict['token'], message_id_unpin['message_id'])

##message remove

chan_id_edit = channels_create(hayden_dict['token'], 'message_edit', True)
channel_invite(hayden_dict['token'], chan_id_edit["channel_id"], rob_dict["u_id"])
channel_invite(hayden_dict['token'], chan_id_edit["channel_id"], FOMO_dict["u_id"])

message_id_edit = message_send(rob_dict['token'], chan_id_edit['channel_id'], "Robs message to be edited")

def test_message_edit_invalid_AccessError1():
    with pytest.raises(AccessError):
        message_edit(FOMO_dict['token'], message_id_edit['message_id'], "this is the new message")

message_edit(rob_dict['token'], message_id_edit['message_id'], "Rob changing robs message")

def test_message_edit():
    assert get_messages_store()['Messages'][6]['message'] == "Rob changing robs message"

message_id_edit2 = message_send(rob_dict['token'], chan_id_edit['channel_id'], "Robs message for Hayden to edit")

message_edit(hayden_dict['token'], message_id_edit2['message_id'], "Hayden changing robs message")

def test_message_edit2():
    assert get_messages_store()['Messages'][7]['message'] == "Hayden changing robs message"



chan_id_remove = channels_create(hayden_dict['token'], 'message_remove', True)
channel_invite(hayden_dict['token'], chan_id_remove["channel_id"], rob_dict["u_id"])
channel_invite(hayden_dict['token'], chan_id_remove["channel_id"], FOMO_dict["u_id"])

message_id_remove = message_send(rob_dict['token'], chan_id_remove['channel_id'], "Robs message to be removed")

def test_message_remove_invalid_AccessError1():
    with pytest.raises(AccessError):
        message_remove(FOMO_dict['token'], message_id_remove['message_id'])

message_id_remove2 = message_send(rob_dict['token'], chan_id_remove['channel_id'], "Robs second message")

message_remove(rob_dict['token'], message_id_remove2['message_id'])

def test_message_remove():
    assert len(get_messages_store()['Messages'])== 9

def test_message_remove_invalid_InputError1():
    with pytest.raises(InputError):
        message_remove(rob_dict['token'], message_id_remove2['message_id'])
