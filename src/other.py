from re import search
from error import InputError
from db import login, make_user, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from db import token_check, channel_check, u_id_check


#works refer to this for GET functions
def users_all(token):

    if not token_check(token):
        print('Token invalid')
        raise InputError
    
    user_store = get_user_store()

    user_dict = {
        'users':[]
    }

    for indiv_user in user_store['users']:
        user_dict['users'].append({'u_id': indiv_user['u_id'], 'email':indiv_user['email'],
        'name_first': indiv_user['name_first'], 'name_last': indiv_user['name_last'], 
        'handle_str': indiv_user['handle_str'] })

    print(user_dict)
    return user_dict

def search(token, query_str):
    # search for all channel ids that the user has joined in message
    # iterate thru message database and append to a new {messages: list} the messages that == user_id
    # remember to reverse the list before returning it
    user = token_check(token)
    message_store = get_messages_store()
    message_list = {
        'messages':[]
    }
    for user_part in user['channel_id_part']:
        for mem_check in message_store["Messages"]:
            if mem_check['channel_id'] == user_part:
                fullstring = mem_check['message']
                substring = query_str
                if substring in fullstring:
                    message_list['messages'].append({'message_id':mem_check['message_id'],'u_id': mem_check['user_id'],
                    'message':mem_check['message'], 'time_created': mem_check['time_created'] })

    message_list['messages'].reverse()
    return message_list
