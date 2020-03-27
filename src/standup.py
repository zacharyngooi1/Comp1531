from db import channel_check, get_channel_store, is_any_other_standup_active
#import message
from datetime import datetime, timezone
from error import InputError
from auth import auth_register
from channel import channels_create

#This function is named standup_start because the standup/start wrapper will be placed around it.
#But really all this function does is return the time_finish and check of the token and channel_id are valid.
def standup_start(token, channel_id, length):
    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    if channel == None:
        return InputError
    if channel['standup']['is_standup_active'] == True:
        raise InputError
    current_moment_in_time = datetime.now()
    time_finish = length + current_moment_in_time.replace(tzinfo=timezone.utc).timestamp()
    channel['standup']['time_standup_finished'] = time_finish
    return {
        'time_finish' : time_finish #This is a unix timestamp
    }

def standup_active(token, channel_id):
    """channel_store = get_channel_store()
    f is_any_other_standup_active(channel_id) == False:
        raise InputError
    flag = 1
    for channel in channel_store['Channels']:
        if channel['channel_id'] == channel_id:
            if channel['standup']['is_standup_active'] == False:
                flag == 0
    for channel in channel_store['Channels']:

    if flag == 0:
        time_finish == None
        is_active = False
    else:
        is_active = True
        time_finish = channel_dict['standup']['time_standup_finished']"""
    return {
        'is_active' : is_active,
        'time_finish' : time_finish
    }

def standup_send(token, channel_id, message):
    return {

    }
input_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(input_dict['token'], 'Hayden', True)
print(standup_start(input_dict['token'], chan_id['channel_id'], 50))
print(get_channel_store())