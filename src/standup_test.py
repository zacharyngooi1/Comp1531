import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channels_create, channel_invite
from standup import standup_start, standup_active, standup_send
from db import get_messages_store, channel_check, get_channel_store, get_standup_queue, token_check
import datetime
from datetime import timezone
import time
#Assumptions
#All the inputs are valid
hayden_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(hayden_dict['token'], 'Hayden', True)
rob_dict = auth_register("rob@gmail.com", "paswword123", "Rob", "Ever")
gary_dict = auth_register("gary@gmail.com", "bary1234", "gary", "bary")
channel_invite(hayden_dict['token'], chan_id["channel_id"], gary_dict["u_id"])

hayden_full_dict = token_check(hayden_dict['token'])
gary_full_dict = token_check(gary_dict['token'])
print(hayden_dict)
#standup_start(hayden_dict['token'], 1, 10) #invalid channel id

def test_standup_start_invalid_InputError1():
    with pytest.raises(InputError):
        standup_start(hayden_dict['token'], 1, 10) #invalid channel id

time_length = 3


standup_start(hayden_dict['token'], chan_id['channel_id'], time_length )
channel = channel_check(chan_id['channel_id'])

final = int(time_length + datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp())
def test_standup_start():
    assert int(channel['standup']['time_standup_finished']) == final



def test_standup_start_invalid_InputError2():
    with pytest.raises(InputError):
        standup_start(hayden_dict['token'], chan_id['channel_id'], time_length )



def test_standup_active_invalid_InputError1():
    with pytest.raises(InputError):
        standup_active(hayden_dict['token'], 1) #invalid channel id


#print(standup_info)

#print(datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp())
def test_standup_active():
    
    standup_info = standup_active(hayden_dict['token'], chan_id['channel_id'] )


    assert standup_info['is_active'] == True
    assert int(standup_info['time_finish']) == final
    



def test_standup_send_invalid_InputError1():
    #time.sleep(time_length)
    with pytest.raises(InputError):
        standup_send(hayden_dict['token'], 1, "Hey wssup helo") #invalid channel id


def test_standup_send_invalid_InputError2():
    #time.sleep(time_length)
    with pytest.raises(InputError):
        standup_send(hayden_dict['token'], chan_id['channel_id'], "1"*1001) #invalid channel id


def test_standup_send():
    
    standup_send(hayden_dict['token'], chan_id['channel_id'], "message 1 ")
    standup_send(hayden_dict['token'], chan_id['channel_id'], "message 2")
    print(get_standup_queue())
    assert get_standup_queue()['Standup_queues'][0]['final_string'] ==  hayden_full_dict['handle_str'] + ':message 1 ,'+hayden_full_dict['handle_str'] +':message 2,'

    time.sleep(time_length)
    standup_start(hayden_dict['token'], chan_id['channel_id'], time_length )
    standup_send(hayden_dict['token'], chan_id['channel_id'], "second time babyyy ")
    standup_send(gary_dict['token'], chan_id['channel_id'], "Does this work")
    standup_send(hayden_dict['token'], chan_id['channel_id'], "ofc it does")

    assert get_standup_queue()['Standup_queues'][1]['final_string'] ==  hayden_full_dict['handle_str'] + ':second time babyyy ,'+gary_full_dict['handle_str'] +':Does this work,' + hayden_full_dict['handle_str'] + ':ofc it does,'

#standup_send(hayden_dict['token'], chan_id['channel_id'], "message 1 ")
#standup_send(hayden_dict['token'], chan_id['channel_id'], "message 2")
#print(get_standup_queue())


def test_standup_send_invalid_AccessError1():
    #time.sleep(time_length)
    with pytest.raises(AccessError):
        standup_send(rob_dict['token'], chan_id['channel_id'], "Hey wassup") #invalid channel id


def test_standup_send_invalid_InputError3():
    time.sleep(time_length)
    with pytest.raises(InputError):
        standup_send(hayden_dict['token'], chan_id['channel_id'], "Hey wassup") #invalid channel id


