from error import InputError, AccessError
from standup import standup_start, standup_active, standup_send
import pytest
from auth import auth_register
from channel import channels_create
from datetime import time, datetime, timezone
import time
from db import get_standup_queue

hayden_dict = auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(hayden_dict['token'], 'Hayden', True)
rob_dict = auth_register('rob@gamil.com', 'password123', 'Rob', 'Everest')
second_chan_id = channels_create(rob_dict['token'], 'Rob', True)


#Test if standup/start works normally
def test_standup_start():
    standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 10)
    time_finish = standup_started["time_finish"]
    time.sleep(10)
    # The time returned must be less than current time by a really small amount
    time_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert time_finish <= time_now

def test_standup_start_wrong_channel_id():
    with pytest.raises(InputError):
        standup_start(hayden_dict['token'], second_chan_id['channel_id'], 50)

def test_standup_start_active_standup():
    standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 50)
    with pytest.raises(InputError):
        standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 50)

#Test if standup/active works normally
def test_standup_active():
    standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 10)
    results_for_standup_active = standup_active(hayden['token'], chan_id['channel_id'])
    assert results_for_standup_active["is_active"] == True
    time.sleep(10)
    time_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert time_finish <= time_now

def test_standup_active_wrong_channel_id():
    standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 10)
    with pytest.raises(InputError):
        standup_active(hayden_dict['token'], second_chan_id['channel_id'])

#Testing if standup/send works normally
def test_standup_send():
    standup_started = standup_start(rob_dict['token'], second_chan_id['channel_id'], 10)
    standup_send(rob_dict['token'], second_chan_id['channel_id'], "Hayden")
    standup_send(rob_dict['token'], second_chan_id['channel_id'], "Smith")
    standup_send(rob_dict['token'], second_chan_id['channel_id'], "Rob")
    standup_queue_store = get_standup_queue()
    assert standup_queue_store['final_string'] == 'haydensmith24200:Hayden\nhaydensmith24200:Smith\nhaydensmith24200:Rob\n'

def test_standup_send_wrong_channel_id():
    standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 10)
    with pytest.raises(InputError):
        standup_send(hayden_dict['token'], second_chan_id['channel_id'], "Hahahaha")

def test_standup_send_large_message():
    standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 10)
    with pytest.raises(InputError):
        standup_send(hayden_dict['token'], chan_id['channel_id'], "Hahahaha"*100000000)

def test_standup_send_no_active_channel():
    with pytest.raises(InputError):
        standup_send(hayden_dict['token'], second_chan_id['channel_id'], "Hahahaha")

def test_standup_send_unauthorised_user():
    standup_started = standup_start(hayden_dict['token'], chan_id['channel_id'], 10)
    with pytest.raises(AccessError):
        standup_send(rob_dict['token'], chan_id['channel_id'], "Hahahaha")
