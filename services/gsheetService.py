import os.path
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants.common import SPREADSHEET_ID
from constants.file import CREDENTIALS_FILE_PATH, SHEET_FILE_PATH, SHEETS, TOKEN_FILE_PATH, V4, VALUES, W, value_input_option

logger = logging.getLogger(__name__)


class GSheetService():

    async def getdata(self, range_name):
        SCOPES = [SHEET_FILE_PATH]
        SAMPLE_SPREADSHEET_ID = SPREADSHEET_ID
        creds = None
        if os.path.exists(TOKEN_FILE_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE_PATH, W) as token:
                token.write(creds.to_json())
        try:
            service = build(SHEETS, V4, credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
            values = result.get(VALUES, [])
        except HttpError as err:
            logger.error(err)
        return values

    async def add(self, data, range_name):
        data = list(data)
        SCOPES = [SHEET_FILE_PATH]
        SAMPLE_SPREADSHEET_ID = SPREADSHEET_ID
        creds = None
        if os.path.exists(TOKEN_FILE_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE_PATH, W) as token:
                token.write(creds.to_json())
        try:
            service = build(SHEETS, V4, credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
            values = result.get(VALUES, [])
            values.append(data)
            body = {
                VALUES: values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
                valueInputOption=value_input_option, body=body).execute()
        except HttpError as err:
            logger.error(err)
        return []
