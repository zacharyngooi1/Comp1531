import message
import channels
import channel
import pytest
from error import InputError
from auth import auth_register

#Assumptions
#All the inputs are valid

#Checks weather the message has been sent
def test_message_send():
     #by default message_id is 1.
    assert message.message_send(12345, 1, 'Hello world') == 1  
    message_id = message.message_send(12345, 1, 'Hello world')
    #check if the message has actually been sent
    assert channel.channel_messages['messages']['message_id'] == 1  
    
#Checks weather the message has been removed
def test_message_remove():
    out = message.message_send(12345, 1, 'hello hru')
    assert message.message_remove(12345,1) == {}

#Checks weather the message has been edited
def test_message_edit():
    out = message.message_send(12345, 1, 'Bye World')
    message_id = message.message_edit(12345, 1, 'Hello world')
    #check if the message has been edit
    assert channel.channel_messages['messages']['message_id'] == "Hello world"  

def test_message_except():
    #an example of when there would be an inout error ie. message longer than 1000
    with pytest.raises(InputError) as e:
        assert message.message_send(12345, 1, 'a'*1001)
    
    #Access error example
    #if someone called Bob tries to access channel    
    list_of_channels = channels_listall(12345)
    flag =1
    if "Bob" in list_of_channels[name]:
        flag = 0
    with pytest.raises(AccessError) as e:
        assert flag == 1
