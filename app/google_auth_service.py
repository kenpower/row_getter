from google.oauth2 import id_token
from google.auth.transport import requests
from flask import request

class GoogleAuthServiceError(Exception):
    def __init__(self, message):
        self.message = message

class GoogleAuthService:
    def __init__(self, CLIENT_ID):
        self.CLIENT_ID = CLIENT_ID

    def get_google_credentials(self, request):
        csrf_token_cookie = request.cookies.get('g_csrf_token')
        if not csrf_token_cookie:
            raise GoogleAuthServiceError('No CSRF token in Cookie.')
        csrf_token_body = request.form['g_csrf_token']
        if not csrf_token_body:
            raise GoogleAuthServiceError('No CSRF token in post body.')
        if csrf_token_cookie != csrf_token_body:
            raise GoogleAuthServiceError('Failed to verify double submit cookie.')
        
        try:
        # Specify the CLIENT_ID of the app that accesses the backend:
            print(request.form['credential'] )
            google_credentials = id_token.verify_oauth2_token(
                request.form['credential'], 
                requests.Request(), 
                self.CLIENT_ID
                )
            return google_credentials
        except ValueError:
            raise GoogleAuthServiceError('Invalid Token')