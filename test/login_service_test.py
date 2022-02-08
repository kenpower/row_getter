import os
import sys
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
#sys.path.append(os.path.abspath('../app'))

import json
from cryptography.fernet import Fernet
import login_service
import user

CRYPTO_KEY_STRING =b'EtaiFUpSYHXf4AdzN9uS1m5etzPhd8oUoX_-kqH1O6o=' # key for testing
CRYPTO_KEY = bytearray(CRYPTO_KEY_STRING)

login_service = login_service.Login_service(CRYPTO_KEY)

def test_login_no_cookie():
    assert None==login_service.get_logged_in_user(None)

def test_login_rubbish_cookie():
    cookie = 'rubbish'
    assert None == login_service.get_logged_in_user(cookie)

def test_login_fake_cookie():
    user_credentials = {'rubbish':'user1', 'gmail':'user@gmail'}
    cookie = login_service.generate_login_cookie(user_credentials)
    assert None==login_service.get_logged_in_user(cookie)

def test_login_good_cookie():
    logged_in_user = user.User('user1', 'user@gmail', 'http://www.google.com/image.jpg')    
    cookie = login_service.generate_login_cookie(logged_in_user)

    user_from_cookie = login_service.get_logged_in_user(cookie)
    
    assert logged_in_user == user_from_cookie

def test_generate_login_cookie():
    aUser = user.User('user1', 'user@gmail', 'http://www.google.com/image.jpg')
    cookie = login_service.generate_login_cookie(aUser)
    print(cookie)
    cipher_suite = Fernet(CRYPTO_KEY)
    decrypt_credentials = json.loads(cipher_suite.decrypt(bytes(cookie, encoding='utf8')))

    assert decrypt_credentials['name'] == aUser.name
    assert decrypt_credentials['gmail'] == aUser.gmail
    assert decrypt_credentials['picture_url'] == aUser.picture_url


def test_generate_user_from_google_credentials():
    google_credentials = {u'picture': u'https://picture_url', u'sub': u'1234', u'name': u'John Smith', u'family_name': u'Smithy', u'iss': u'https://accounts.google.com', u'email_verified': True, u'nbf': 1639349541, u'jti': u'89898989', u'given_name': u'Johnny', u'exp': 1639353441, u'azp': u'xyz', u'iat': 1639349841, u'email': u'js@gmail.com', u'aud': u'xyxyx_audience.googleusercontent.com'}
    user = login_service.user_from_google_credentials(google_credentials)
    assert user.name == google_credentials['name']
    assert user.gmail == google_credentials['email']
    assert user.picture_url == google_credentials['picture']

    # {u'picture': u'https://lh3.googleusercontent.com/a-/AOh14GirG6l9tljR2Bj0V1ZlJn9immSTnHStFjldw7_xxxxxx', u'sub': u'xxxxxx34029046', u'name': u'Ken Power', u'family_name': u'Power', u'iss': u'https://accounts.google.com', u'email_verified': True, u'nbf': 1639349541, u'jti': u'4f879a7e0d893322d25ba5266ca71ebf11e9c4e8', u'given_name': u'Ken', u'exp': 1639353441, u'azp': u'633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com', u'iat': 1639349841, u'email': u'gmail@gmail.com', u'aud': u'633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com'}