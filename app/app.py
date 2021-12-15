#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from flask import Flask, g, request, render_template, abort, make_response, redirect
import json
from functools import wraps
from login_service import LoginService
from google_sheets_service import GoogleSheetsService
from google_auth_service import GoogleAuthService, GoogleAuthServiceError
from user_service import UserDataService
from exceptions import *

SIGN_IN_WITH_GOOGLE_CLIENT_ID="633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com"

PROD = os.environ.get('PROD')
if PROD:
  DOMAIN = os.environ.get("DOMAIN")
  CRYPTO_KEY_STRING =  os.environ.get("CRYPTO_KEY")
  #GOOGLE_PRIVATE_KEY =  os.environ.get("GOOGLE_PRIVATE_KEY")
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

def login_user(handler):
  @wraps(handler)
  def wrapper(*args, **kwargs):  
    user =  login_service.get_logged_in_user(request.cookies.get('login'))
    if(user is None):  
      return render_template('signin.html', \
        DOMAIN=DOMAIN, CLIENT_ID=SIGN_IN_WITH_GOOGLE_CLIENT_ID)
    g.user = user
    return handler(*args, **kwargs)

  return wrapper

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

@app.route('/test')
def testpage():
    return "I'm alive!"
  
@app.route('/')
@login_user
def main():
  return get_sheet_rows_for(g.user)

@app.route('/g/<google_sheet_id>')
@login_user
def with_google_sheet_id(google_sheet_id):
  return get_sheet_rows_for(g.user, google_sheet_id)

def get_sheet_rows_for(user, google_sheet_id = None):
  try:
    if google_sheet_id is None:  
      data = user_data_service.get_user_data_from_sheet(user.gmail)
    else:
      data = user_data_service.get_user_data_from_sheet(user.gmail, google_sheet_id)
    return render_template('results.html', table_data = data, user = user)
  except SpreadSheetNotFoundError as e:
    error=f"{google_sheet_id} is not a valid Google doc ID"
  except NotAGooogleSpreadSheetError as e:
    error=f"{google_sheet_id} is not a Google Sheet (might be a xlxs sheet stored in gDrive)"
  except PermissionDeniedError as e:
    error=f"{google_sheet_id} is not shared with this app (it needs to be shared with  'row-getter-service@row-getter.iam.gserviceaccount.com')"
  
  return render_template('error.html',message = error)
if __name__ == '__main__':
    app.run()