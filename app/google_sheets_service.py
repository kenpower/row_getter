import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
class GoogleSheetsService:
    def __init__(self, credentials_file_path):
        service_account_info = json.load(open(credentials_file_path))
        #https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html
        self.credentials = Credentials.from_service_account_info(\
            service_account_info)
        self.resource =  build('sheets', 'v4', credentials = self.credentials)

    def get_sheet_values(self, spreadsheet_id, range):
        sheet=self.resource.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range).execute()
        values = result.get('values', [])
        return values