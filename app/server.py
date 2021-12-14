#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from flask import Flask, request, render_template, jsonify, abort, make_response, redirect
import test
import os.path
import json
import login_service
import google_sheets_service
from google_auth_service import Google_auth_service, GoogleAuthServiceError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1HKlFYiyL6IGTsGHBtAnwNfzo0tkmO5wTm-8Avp-m5zM'
SAMPLE_RANGE_NAME = 'A1:ZZ10000'
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

login_service = login_service.Login_service(CRYPTO_KEY)
google_sheets_service = google_sheets_service.Google_sheets_service('.data/row-getter-service-account-google.json')
google_auth_service = Google_auth_service(SIGN_IN_WITH_GOOGLE_CLIENT_ID)

@app.route('/test')
def testpage():
    return os.environ.get("CRYPTO_KEY")

@app.route('/main')
def homepage():
    """Displays the homepage."""
    return render_template('index.html')
  
@app.route('/')
def signin():
  user =  login_service.get_logged_in_user(request.cookies.get('login'))
  if(user is None):  
    return render_template('signin.html', DOMAIN=DOMAIN, CLIENT_ID=SIGN_IN_WITH_GOOGLE_CLIENT_ID)
  return get_rows(user)

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
  
  
def get_rows(user):  
    values = google_sheets_service.get_sheet_values(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
    filteredvalues=[values[0]]
    
    for row in values[1:]:
      if(user.gmail == row[0]):
        filteredvalues.append(row)    
        
    return render_template('results.html', table_data = filteredvalues, idinfo = user)
  
if __name__ == '__main__':
    app.run()