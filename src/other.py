def users_all(token):
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
            {
                'u_id': 2,
        	    'email': 'zachary@cse.unsw.edu.au',
        	    'name_first': 'Zach',
        	    'name_last': 'Ngooi',
        	    'handle_str': 'NZach',
            },
        ],
    }

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
