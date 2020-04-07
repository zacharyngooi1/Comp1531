import json
import requests
import urllib.request
import pytest
from db import get_user_store, get_messages_store, get_channel_store
from error import InputError, AccessError, NameException, KeyError

BASE_URL = "http://127.0.0.1:53251"

def test_messages_send():

    requests.get(f"{BASE_URL}/reset")


    r = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "zacharyngooi@hotmail.com",
        "password": "password",
        "name_first" : "hayden",
        "name_last" : "smith",
    })

    wrong_user = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first" : "john",
        "name_last" : "smith",
    })

    payload = r.json()
    payload_wrong_user = wrong_user.json()
    assert payload["u_id"] != None
    assert payload["token"] != None
    assert payload_wrong_user["u_id"] != None
    assert payload_wrong_user["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":r["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    m = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message"
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None
    
    with pytest.raises(InputError):
        m = requests.post(f"{BASE_URL}/message/send", json={
            "token":payload["token"],
            "channel_id":payload_2["channel_id"],
            "message": "Wrong message"* 10001
        })
    
    with pytest.raises(AccessError):
        m = requests.post(f"{BASE_URL}/message/send", json={
            "token":payload_wrong_user["token"],
            "channel_id":payload_2["channel_id"],
            "message": "Hello"
        })

def test_message_sendlater():
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "zacharyngooi@hotmail.com",
        "password": "password",
        "name_first" : "hayden",
        "name_last" : "smith",
    })

    wrong_user = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first" : "john",
        "name_last" : "smith",
    })

    payload = r.json()
    payload_wrong_user = wrong_user.json()
    assert payload["u_id"] != None
    assert payload["token"] != None
    assert payload_wrong_user["u_id"] != None
    assert payload_wrong_user["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":payload["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    m = requests.post(f"{BASE_URL}/message/sendlater", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message",
        "time_sent": 120
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None
    
    with pytest.raises(InputError):
        m = requests.post(f"{BASE_URL}/message/sendlater", json={
            "token":payload["token"],
            "channel_id":payload_2["channel_id"],
            "message": "Wrong message"* 10001,
            "time_sent": 120
        })
        m = requests.post(f"{BASE_URL}/message/sendlater", json={
            "token":payload["token"],
            "channel_id":1,
            "message": "Hello",
            "time_sent": 120
        })
        m = requests.post(f"{BASE_URL}/message/sendlater", json={
            "token":payload["token"],
            "channel_id":payload_2["channel_id"],
            "message": "Hello",
            "time_sent": -10
        })

    with pytest.raises(AccessError):
        m = requests.post(f"{BASE_URL}/message/sendlater", json={
            "token":payload_wrong_user["token"],
            "channel_id":payload_2["channel_id"],
            "message": "Hello",
            "time_sent": 120
        })

def test_message_react():
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "zacharyngooi@hotmail.com",
        "password": "password",
        "name_first" : "hayden",
        "name_last" : "smith",
    })

    payload = r.json()
    assert payload["u_id"] != None
    assert payload["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":payload["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    m = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message"
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None

    m_react = requests.post(f"{BASE_URL}/message/react", json = {
        "token": payload["token"],
        "message_id": payload_3["message_id"],
        "react_id": 1
    })
    
    payload_4 = m_react.json()
    assert payload_4 == {}

    with pytest.raises(InputError):
        m_react = requests.post(f"{BASE_URL}/message/react", json={
            "token":payload["token"],
            "message_id":-10,
            "react_id":1
        })
        m_react = requests.post(f"{BASE_URL}/message/react", json={
            "token":payload["token"],
            "message_id":payload_3["message_id"],
            "react_id":100
        })

    with pytest.raises(InputError):
        m_react = requests.post(f"{BASE_URL}/message/react", json={
            "token":payload["token"],
            "message_id":-10,
            "react_id":1
        })

def test_message_unreact():
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "zacharyngooi@hotmail.com",
    "password": "password",
    "name_first" : "hayden",
    "name_last" : "smith",
    })

    payload = r.json()
    assert payload["u_id"] != None
    assert payload["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":payload["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    m = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message"
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None

    m_react = requests.post(f"{BASE_URL}/message/react", json = {
        "token": payload["token"],
        "message_id": payload_3["message_id"],
        "react_id": 1
    })

    payload_4 = m_react.json()
    assert payload_4 == {}

    with pytest.raises(InputError):
        m_react = requests.post(f"{BASE_URL}/message/unreact", json={
            "token":payload["token"],
            "message_id":payload_3["message_id"],
            "react_id":0
        })
    
    m_unreact = requests.post(f"{BASE_URL}/message/unreact", json = {
        "token": payload["token"],
        "message_id": payload_3["message_id"],
        "react_id": 0
    })

    payload_5 = m_unreact.json()
    assert payload_5 == {}

    with pytest.raises(InputError):
        m_react = requests.post(f"{BASE_URL}/message/unreact", json={
            "token":payload["token"],
            "message_id":-10,
            "react_id":1
        })
        m_react = requests.post(f"{BASE_URL}/message/unreact", json={
            "token":payload["token"],
            "message_id":payload_3["message_id"],
            "react_id":0
        })

    with pytest.raises(InputError):
        m_react = requests.post(f"{BASE_URL}/message/unreact", json={
            "token":payload["token"],
            "message_id":-10,
            "react_id":1
        })

def test_message_pin():
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "zacharyngooi@hotmail.com",
    "password": "password",
    "name_first" : "hayden",
    "name_last" : "smith",
    })

    payload = r.json()
    assert payload["u_id"] != None
    assert payload["token"] != None

    another_user = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "johnsmith@gmail.com",
    "password": "password1234",
    "name_first" : "john",
    "name_last" : "smith",
    })

    payload_another = another_user.json()
    assert payload_another["u_id"] != None
    assert payload_another["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":r["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    wrong_user = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "johnsmith@gmail.com",
    "password": "password123",
    "name_first" : "john",
    "name_last" : "smith",
    })
    payload_wrong_user = wrong_user.json()
    assert payload_wrong_user["u_id"] != None
    assert payload_wrong_user["token"] != None


    m = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message"
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None

    m_pin = requests.post(f"{BASE_URL}/message/pin", json={
            "token":payload["token"],
            "message_id":payload_3["message_id"]
        })
    with pytest.raises(InputError):
        m_pin = requests.post(f"{BASE_URL}/message/pin", json={
            "token":payload["token"],
            "message_id":-10,
        })
        m_pin = requests.post(f"{BASE_URL}/message/pin", json={
            "token":payload_wrong_user["token"],
            "message_id":-10,
        })
        m_pin = requests.post(f"{BASE_URL}/message/pin", json={
            "token":payload["token"],
            "message_id":payload_3["message_id"]
        })
    
    with pytest.raises(AccessError):
        m_pin = requests.post(f"{BASE_URL}/message/pin", json={
            "token":payload_wrong_user["token"],
            "message_id":-10,
        })

def test_message_unpin():
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "zacharyngooi@hotmail.com",
    "password": "password",
    "name_first" : "hayden",
    "name_last" : "smith",
    })

    payload = r.json()
    assert payload["u_id"] != None
    assert payload["token"] != None

    another_user = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "johnsmith@gmail.com",
    "password": "password1234",
    "name_first" : "john",
    "name_last" : "smith",
    })

    payload_another = another_user.json()
    assert payload_another["u_id"] != None
    assert payload_another["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":r["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    wrong_user = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "johnsmith@gmail.com",
    "password": "password123",
    "name_first" : "john",
    "name_last" : "smith",
    })
    payload_wrong_user = wrong_user.json()
    assert payload_wrong_user["u_id"] != None
    assert payload_wrong_user["token"] != None


    m = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message"
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None

    m_pin = requests.post(f"{BASE_URL}/message/unpin", json={
            "token":payload["token"],
            "message_id":payload_3["message_id"]
        })
    with pytest.raises(InputError):
        m_pin = requests.post(f"{BASE_URL}/message/unpin", json={
            "token":payload["token"],
            "message_id":-10,
        })
        m_pin = requests.post(f"{BASE_URL}/message/unpin", json={
            "token":payload_wrong_user["token"],
            "message_id":-10,
        })
        m_pin = requests.post(f"{BASE_URL}/message/unpin", json={
            "token":payload["token"],
            "message_id":payload_3["message_id"]
        })
    
    with pytest.raises(AccessError):
        m_pin = requests.post(f"{BASE_URL}/message/unpin", json={
            "token":payload_wrong_user["token"],
            "message_id":-10,
        })

def message_remove():
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "zacharyngooi@hotmail.com",
    "password": "password",
    "name_first" : "hayden",
    "name_last" : "smith",
    })

    payload = r.json()
    assert payload["u_id"] != None
    assert payload["token"] != None

    another_user = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "johnsmith@gmail.com",
    "password": "password1234",
    "name_first" : "john",
    "name_last" : "smith",
    })

    payload_another = another_user.json()
    assert payload_another["u_id"] != None
    assert payload_another["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":r["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    wrong_user = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "johnsmith@gmail.com",
    "password": "password123",
    "name_first" : "john",
    "name_last" : "smith",
    })
    payload_wrong_user = wrong_user.json()
    assert payload_wrong_user["u_id"] != None
    assert payload_wrong_user["token"] != None


    m = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message"
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None

    another_message = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The second message"
    })

    payload_4 = another_message.json()
    assert payload_4["message_id"] != None

    message_remove = requests.post(f"{BASE_URL}/message/remove", json = {
        "token": payload["token"],
        "message_id": payload_4["message_id"]
    })

    with pytest.raises(InputError):
        message_remove = requests.post(f"{BASE_URL}/message/remove", json = {
            "token": payload["token"],
            "message_id": payload_4["message_id"]
        })
    
    with pytest.raises(AccessError):
        message_remove = requests.post(f"{BASE_URL}/message/remove", json = {
            "token": wrong_user["token"],
            "message_id": payload_4["message_id"]
        }) # This owner is not an authorised user of the owner
    
def message_edit():
    requests.get(f"{BASE_URL}/reset")

    r = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "zacharyngooi@hotmail.com",
    "password": "password",
    "name_first" : "hayden",
    "name_last" : "smith",
    })

    payload = r.json()
    assert payload["u_id"] != None
    assert payload["token"] != None

    another_user = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "johnsmith@gmail.com",
        "password": "password1234",
        "name_first" : "john",
        "name_last" : "smith",
    })

    payload_another = another_user.json()
    assert payload_another["u_id"] != None
    assert payload_another["token"] != None

    c = requests.post(f"{BASE_URL}/channels/create", json = {
        "token":r["token"],
        "name":"thisIsANewChannel",
        "is_public": True
    })

    payload_2 = c.json()
    assert payload_2["channel_id"] != None

    wrong_user = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first" : "john",
        "name_last" : "smith",
    })
    payload_wrong_user = wrong_user.json()
    assert payload_wrong_user["u_id"] != None
    assert payload_wrong_user["token"] != None


    m = requests.post(f"{BASE_URL}/message/send", json = {
        "token": payload["token"],
        "channel_id": payload_2["channel_id"],
        "message": "The first message"
    })

    payload_3 = m.json()
    assert payload_3["message_id"] != None

    edited_message = requests.post(f"{BASE_URL}/message/edit", json = {
        "token": payload["token"],
        "message": payload_3["message_id"],
        "message": "The second message"
    })

    payload_4 = edited_message.json()
    assert payload_4["message_id"] != None

    with pytest.raises(AccessError):
        message_remove = requests.post(f"{BASE_URL}/message/edit", json = {
            "token": wrong_user["token"],
            "message_id": payload_3["message_id"]
            "message": "The second message"
        }) # This owner is not an authorised user of the owner
    
