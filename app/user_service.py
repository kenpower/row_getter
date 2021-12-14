
SAMPLE_SPREADSHEET_ID = '1HKlFYiyL6IGTsGHBtAnwNfzo0tkmO5wTm-8Avp-m5zM'
SAMPLE_RANGE_NAME = 'A1:ZZ10000'

class UserDataService:
    def __init__(self, google_sheets_service):
        self.google_sheets_service = google_sheets_service

    def get_user_data_from_sheet(self, gmail):
        values = self.google_sheets_service.get_sheet_values(\
            SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
        
        filteredvalues=[values[0]] #take 1st row as headers
        
        for row in values[1:]:
            if(gmail == row[0]):
                filteredvalues.append(row) 

        return filteredvalues

