
SAMPLE_SPREADSHEET_ID = '1HKlFYiyL6IGTsGHBtAnwNfzo0tkmO5wTm-8Avp-m5zM'
SAMPLE_RANGE_NAME = 'A1:ZZ10000'

class UserDataService:
    def __init__(self, google_sheets_service):
        self.google_sheets_service = google_sheets_service

    def get_user_data_from_sheet(self, gmail, sheet_id = SAMPLE_SPREADSHEET_ID, range_name = SAMPLE_RANGE_NAME):
        values = self.google_sheets_service.get_sheet_values(\
            sheet_id, range_name)
        
        filteredvalues=[values[0]] #take 1st row as headers
        
        for row in values[1:]:
            if(gmail == row[0]):
                filteredvalues.append(row) 

        return filteredvalues

