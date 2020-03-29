from db import channel_check, get_channel_store, message_send_for_standup, get_standup_queue, member_channel_check, token_check
from datetime import datetime, timezone
import time
from error import InputError
from auth import auth_register
from channel import channels_create
from error import AccessError, InputError
from db import get_standup_queue
#This function is named standup_start because the standup/start wrapper will be placed around it.
#But really all this function does is return the time_finish and check of the token and channel_id are valid.
#"final_string":""
def standup_start(token, channel_id, length):
    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    if channel == False:
        raise InputError
    current_moment_in_time = datetime.now()

    if channel['standup']['time_standup_finished'] != None:
        if current_moment_in_time.replace(tzinfo=timezone.utc).timestamp() < channel['standup']['time_standup_finished']:
            raise InputError
    get_standup_queue()['Standup_queues'].append({"final_string":""})
    channel['standup']['is_standup_active'] = True
    time_finish = length + current_moment_in_time.replace(tzinfo=timezone.utc).timestamp()
    channel['standup']['time_standup_finished'] = time_finish
    return {
        'time_finish' : time_finish #This is a unix timestamp
    }

def standup_active(token, channel_id):
    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    if channel == False:
        raise InputError
    current_moment_in_time = datetime.now()
    print("now:",current_moment_in_time.replace(tzinfo=timezone.utc).timestamp())
    print("then:",channel['standup']['time_standup_finished'])
    if current_moment_in_time.replace(tzinfo=timezone.utc).timestamp() < channel['standup']['time_standup_finished']:
        return {
            'is_active' : True,
            'time_finish' : channel['standup']['time_standup_finished']
        }
    return {
        'is_active' : False,
        'time_finish' : None
    }
    

def standup_send(token, channel_id, message):
    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    if channel == False:
        raise InputError
    if member_channel_check(token, channel_id) == False:
        raise AccessError
    if len(message) > 1000:
        raise InputError
    if standup_active(token,channel_id)['is_active'] == False:
        raise InputError
    user = token_check(token)
    if channel['standup']['time_standup_finished'] - datetime.now().replace(tzinfo=timezone.utc).timestamp() > 0:
        message_send_for_standup(user['u_id'], message)
    return {
    
    }

"""
input_dict = auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
print(get_channel_store())
chan_id = channels_create(input_dict['token'], 'Hayden', True)
print(standup_start(input_dict['token'], chan_id['channel_id'], 50))
print()
print("printing standup_active")
print(get_channel_store())
print(standup_active(input_dict['token'], chan_id['channel_id']))
print()
print(get_channel_store())
print()
standup_send(input_dict['token'], chan_id['channel_id'], "Hayden")
time.sleep(51)
standup_send(input_dict['token'], chan_id['channel_id'], "Smith")
standup_send(input_dict['token'], chan_id['channel_id'], "Rob")
standupqueue_store = get_standup_queue()
print(standupqueue_store)
"""
