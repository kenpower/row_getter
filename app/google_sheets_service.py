import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

from exceptions import *
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
        try:
            result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range).execute()
            print("got ss data")
            values = result.get('values', [])
            return values
        except HttpError  as e:
            if e.resp.get('content-type', '').startswith('application/json'):
                reason = json.loads(e.content).get('error').get('status')
                code = json.loads(e.content).get('error').get('code')
                print(f'Error: {code=} {reason=} ')
                if reason == 'NOT_FOUND':
                    raise SpreadSheetNotFoundError(f'Spreadsheet {spreadsheet_id} not found')
                if reason == 'FAILED_PRECONDITION':
                    raise NotAGooogleSpreadSheetError(f'Spreadsheet {spreadsheet_id} is not a google sheet')
                if reason == 'PERMISSION_DENIED':
                    raise PermissionDeniedError(f'Permission denied for spreadsheet {spreadsheet_id}')   
            raise SomeUnknownGooogleSpreadSheetError(f'Unknown google sheet error {e}')


#e.resp.content =>
# {'error': 
#   {
#   'code': 404, 
#   'message': 'Requested entity was not found.', 
#   'errors': [
#       {
#       'message': 'Requested entity was not found.', 
#       'domain': 'global', 
#       'reason': 'notFound'
#       }
#   ], 
#   'status': 'NOT_FOUND'}
# }


