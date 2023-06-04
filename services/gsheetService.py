import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GSheetService():

    def getdata(self):
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        SAMPLE_SPREADSHEET_ID = '1lbczudmolZeFCVqpjF1EwFyxAKANFuI_Co6KmVgOMDo'

        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range="Sheet2").execute()
            values = result.get('values', [])

        except HttpError as err:
            print(err)
            
        return  values

    def add(self,data):
        data = list(data)
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        SAMPLE_SPREADSHEET_ID = '1lbczudmolZeFCVqpjF1EwFyxAKANFuI_Co6KmVgOMDo'

        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range="Sheet1").execute()
            values = result.get('values', [])
            values.append(data)

            body = {
            'values': values
            }


            result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1",
            valueInputOption="USER_ENTERED", body=body).execute()

        except HttpError as err:
            print(err)
        return []


