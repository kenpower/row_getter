#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from flask import Flask, request, render_template, jsonify, abort
import test
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import id_token
from google.auth.transport import requests


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-ezwh3gMwm4aVD-NT22q3nTFlPYpsFGFbW2q8UEHBiY'
SAMPLE_RANGE_NAME = 'A2:E100'


# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

# Dream database. Store dreams in memory for now. 
DREAMS = ['Python. Python, everywhere.']


@app.after_request
def apply_kr_hello(response):
    """Adds some headers to all responses."""
  
    # Made by Kenneth Reitz. 
    if 'MADE_BY' in os.environ:
        response.headers["X-Was-Here"] = os.environ.get('MADE_BY')
    
    # Powered by Flask. 
    response.headers["X-Powered-By"] = os.environ.get('POWERED_BY')
    return response


@app.route('/main')
def homepage():
    """Displays the homepage."""
    return render_template('index.html')
  
@app.route('/')
def signin():
   return render_template('signin.html')

@app.route('/id', methods=['GET', 'POST'])
def id():
  #return jsonify(str(request.data)+str(request.cookies)+ str(request.form))
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
    idinfo = id_token.verify_oauth2_token(request.form['credential'], requests.Request(), "633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com")

    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.
    userid = idinfo['sub']
  except ValueError:
       abort(400, 'Invalid Token')
      
  return jsonify(str(idinfo))
  

@app.route('/lol')
def rlol():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    #print("Google:" + os.environ.get('GOOGLE_PRIVATE_KEY'))
    service_account_info = json.load(open('.data/service_account.json'))
    creds = Credentials.from_service_account_info(service_account_info)
    
    # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    return jsonify(values)
  
@app.route('/dreams', methods=['GET', 'POST'])
def dreams():
    """Simple API endpoint for dreams. 
    In memory, ephemeral, like real dreams.
    """
  
    # Add a dream to the in-memory database, if given. 
    if 'dream' in request.args:
        DREAMS.append(request.args['dream'])
    
    # Return the list of remembered dreams. 
    return jsonify(DREAMS)

if __name__ == '__main__':
    app.run()