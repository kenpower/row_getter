#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from flask import Flask, request, render_template, jsonify, abort
import test
import os.path
import json
import login_service

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import id_token
from google.auth.transport import requests




# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1HKlFYiyL6IGTsGHBtAnwNfzo0tkmO5wTm-8Avp-m5zM'
SAMPLE_RANGE_NAME = 'A1:ZZ10000'

PROD = os.environ.get('PROD')
if PROD:
  DOMAIN = os.environ.get("DOMAIN")
  CRYPTO_KEY_STRING =  os.environ.get("CRYPTO_KEY")
  GOOGLE_PRIVATE_KEY =  os.environ.get("GOOGLE_PRIVATE_KEY")
else:
  DOMAIN = 'http://localhost:5000'
  CRYPTO_KEY_STRING =b'EtaiFUpSYHXf4AdzN9uS1m5etzPhd8oUoX_-kqH1O6o=' # key for testing
  #CRYPTO_KEY_STRING =b'TESTING_KEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=' # key for testing
CRYPTO_KEY = bytearray(CRYPTO_KEY_STRING)

CLIENT_ID="633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com"

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

login_service = login_service.Login_service(CRYPTO_KEY)

@app.route('/test')
def testpage():
    return os.environ.get("CRYPTO_KEY")

@app.route('/main')
def homepage():
    """Displays the homepage."""
    return render_template('index.html')
  
@app.route('/')
def signin():
  if(not login_service.loggedIn(request.cookies.get('login'))):  
    return render_template('signin.html', DOMAIN=DOMAIN, CLIENT_ID=CLIENT_ID)
  return get_rows(idinfo)

@app.route('/id', methods=['GET', 'POST'])
def id():
  csrf_token_cookie = request.cookies.get('g_csrf_token')
  if not csrf_token_cookie:
      abort(400, 'No CSRF token in Cookie.')
  csrf_token_body = request.form['g_csrf_token']
  if not csrf_token_body:
      abort(400, 'No CSRF token in post body.')
  if csrf_token_cookie != csrf_token_body:
      abort(400, 'Failed to verify double submit cookie.')
  try:
    # Specify the CLIENT_ID of the app that accesses the backend:
    idinfo = id_token.verify_oauth2_token(
      request.form['credential'], 
      requests.Request(), 
      CLIENT_ID
      )
  except ValueError:
       abort(400, 'Invalid Token')

  #write a cookie
  #redirect to /  
  # from flask import make_response
  # if s.setSession():
  #     response = make_response(redirect('/home'))
  #     response.set_cookie('session_id', s.session_id)
  #     return response   
  return get_rows(idinfo)
  
  
def get_rows(idinfo):  
    sheet=sheet_service().spreadsheets()
  
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    
    filteredvalues=[values[0]]
    
    for row in values[1:]:
      if(idinfo['email'] == row[0]):
        filteredvalues.append(row)    
        
    return render_template('results.html', table_data = filteredvalues, idinfo = idinfo)

def sheet_service():
    creds = None
    service_account_info = json.load(open('.data/row-getter-service-account-google.json'))
    creds = Credentials.from_service_account_info(service_account_info)
    return build('sheets', 'v4', credentials=creds)
  
if __name__ == '__main__':
    app.run()