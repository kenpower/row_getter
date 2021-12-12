from cryptography.fernet import Fernet
import json
from flask import Flask, request

class Login_service:
    def __init__(self, CRYPTO_KEY):
        self.CRYPTO_KEY = CRYPTO_KEY

    def generateLoginCookie(self, user_credentials):
        cred_bytes = bytes(json.dumps(user_credentials),  encoding='utf8')
        cipher_suite = Fernet(self.CRYPTO_KEY)
        return cipher_suite.encrypt(cred_bytes).decode('utf-8')
    
    def loggedIn(self, login_cookie):
        #login_cookie = request.cookies.get('login')
        if login_cookie is None: 
            return False

        cipher_suite = Fernet(self.CRYPTO_KEY)
        
        try:
            user_credentials = json.loads(cipher_suite.decrypt(bytes(login_cookie, encoding='utf8')))
            if user_credentials['username'] is not None and user_credentials['gmail'] is not None:
                return True 
        except Exception as e:
            print(e) 
        return False