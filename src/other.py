import re
from error import InputError
from auth import auth_login, auth_register, auth_logout
from db import login, make_user, channel_add_all_members, get_channel_store, get_messages_store
from db import get_user_store, add_user, login, make_user
from db import token_check, channel_check, u_id_check


def users_all(token):

user_store = get_user_store()

user_dict = {
    'users':[]
}

for indiv_user in user_store['users']:
    user_dict['users'].append({'u_id': indiv_user['u_id'], 'email':indiv_user['email'],
    'name_first': indiv_user['name_first'], 'name_last': indiv_user['name_last'], 
    'handle_str': indiv_user['handle_str'] })

return user_dict

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
