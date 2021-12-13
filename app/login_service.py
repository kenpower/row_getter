from cryptography.fernet import Fernet
import json
from flask import Flask, request
from user import User

class Login_service:
    def __init__(self, CRYPTO_KEY):
        self.CRYPTO_KEY = CRYPTO_KEY

    def generate_login_cookie(self, user):
        user_json = json.dumps(user, default=lambda o: o.__dict__)
        cred_bytes = bytes(user_json,  encoding='utf8')
        cipher_suite = Fernet(self.CRYPTO_KEY)
        return cipher_suite.encrypt(cred_bytes).decode('utf-8')
    
    def get_logged_in_user(self, encrypted_login_cookie):
        #login_cookie = request.cookies.get('login')
        if encrypted_login_cookie is None: 
            return None

        cipher_suite = Fernet(self.CRYPTO_KEY)
        
        try:
            user_credentials = json.loads(cipher_suite.decrypt(bytes(encrypted_login_cookie, encoding='utf8')))
            if user_credentials is not None:
                return self.user_from_cookie(user_credentials) 
        except Exception as e:
            print(e) 
        return None

    def user_from_cookie(self, cookie):
        try:
            return User(
                cookie['name'], 
                cookie['gmail'],
                cookie['picture_url']
                )
        except KeyError as e: 
            print(e)
            return None

    def user_from_google_credentials(self, google_credentials):
        try:
            return User(
                google_credentials['name'], 
                google_credentials['email'],
                google_credentials['picture']
                )
        except KeyError as e: 
            print(e)
            return None

    
