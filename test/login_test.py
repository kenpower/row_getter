import os
import sys
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
#sys.path.append(os.path.abspath('../app'))
from flask import Flask, request 
from werkzeug.http import dump_cookie
import json
from cryptography.fernet import Fernet
import login_service

app = Flask(__name__)

CRYPTO_KEY_STRING =b'EtaiFUpSYHXf4AdzN9uS1m5etzPhd8oUoX_-kqH1O6o=' # key for testing
CRYPTO_KEY = bytearray(CRYPTO_KEY_STRING)

login_service = login_service.Login_service(CRYPTO_KEY)

def test_login_no_cookie():
    assert False==login_service.loggedIn(None)

def test_login_rubbish_cookie():
    cookie = 'rubbish'
    #with app.test_request_context(environ_base={'HTTP_COOKIE': header}):
    assert False == login_service.loggedIn(cookie)

def test_login_fake_cookie():
    user_credentials = {'rubbish':'user1', 'gmail':'user@gmail'}
    cookie = login_service.generateLoginCookie(user_credentials)
    assert False==login_service.loggedIn(cookie)

def test_login_good_cookie():
    user_credentials = {'username':'user1', 'gmail':'user@gmail'}
    cookie = login_service.generateLoginCookie(user_credentials)
    assert True == login_service.loggedIn(cookie)

def test_generate_login_cookie():
    user_credentials = {'username':'user1', 'gmail':'user@gmail'}
    cookie = login_service.generateLoginCookie(user_credentials)
    print(cookie)
    cipher_suite = Fernet(CRYPTO_KEY)
    decrypt_credentials = json.loads(cipher_suite.decrypt(bytes(cookie, encoding='utf8')))

    assert decrypt_credentials == user_credentials