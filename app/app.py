#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from flask import Flask, request, render_template, jsonify, abort, make_response, redirect
import test
import os.path
import json
from login_service import LoginService
from google_sheets_service import GoogleSheetsService
from google_auth_service import GoogleAuthService, GoogleAuthServiceError
from user_service import UserDataService

#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SIGN_IN_WITH_GOOGLE_CLIENT_ID="633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com"

PROD = os.environ.get('PROD')
if PROD:
  DOMAIN = os.environ.get("DOMAIN")
  CRYPTO_KEY_STRING =  os.environ.get("CRYPTO_KEY")
  GOOGLE_PRIVATE_KEY =  os.environ.get("GOOGLE_PRIVATE_KEY")
else:
  DOMAIN = 'http://localhost:5000'
  CRYPTO_KEY_STRING =b'EtaiFUpSYHXf4AdzN9uS1m5etzPhd8oUoX_-kqH1O6o=' # key for testing

CRYPTO_KEY = bytearray(CRYPTO_KEY_STRING)

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

login_service = LoginService(CRYPTO_KEY)
google_sheets_service = GoogleSheetsService(\
  '.data/row-getter-service-account-google.json')
google_auth_service = GoogleAuthService(SIGN_IN_WITH_GOOGLE_CLIENT_ID)
user_data_service = UserDataService(google_sheets_service)

@app.route('/test')
def testpage():
    return "I'm alive!"
  
@app.route('/')
def signin():
  user =  login_service.get_logged_in_user(request.cookies.get('login'))
  if(user is None):  
    return render_template('signin.html', \
      DOMAIN=DOMAIN, CLIENT_ID=SIGN_IN_WITH_GOOGLE_CLIENT_ID)
  return get_sheet_rows_for(user)

@app.route('/google_sign_in', methods=['GET', 'POST'])
def google_sign_in():
  try:
    google_credentials = google_auth_service.get_google_credentials(request)
  except GoogleAuthServiceError as e:
    abort(400, f"Google Authentication Error: {e.message}")

  user = login_service.user_from_google_credentials(google_credentials)

  response = make_response(redirect('/'))
  response.set_cookie('login',  login_service.generate_login_cookie(user))
  return response
  
  
def get_sheet_rows_for(user):  
    data = user_data_service.get_user_data_from_sheet(user.gmail)
    return render_template('results.html', table_data = data, idinfo = user.name)
  
if __name__ == '__main__':
    app.run()