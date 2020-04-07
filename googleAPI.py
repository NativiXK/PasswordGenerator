from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class SpreadSheets:

    def __init__(self):
        """"
        Cria conexão com a API do google Sheets
        """
        # If modifying these scopes, delete the file token.pickle.
        self.__SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.__SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        print("-Criando serviço de acesso")
        self.__service = build('sheets', 'v4', credentials=creds)

        # The ID and range of a sample spreadsheet.
        if os.path.exists('./userbank.pickle'):
            with open('userbank.pickle', 'rb') as file:
                self.__SPREADSHEET_ID = pickle.load(file)
        else:
            # criando spreadsheet userbank
            print("-Criando banco de dados")
            spreadsheet = {
                'properties': {
                    'title': 'userbank'
                }
            }
            spreadsheet = self.__service.spreadsheets().create(body=spreadsheet,
                                                        fields='spreadsheetId').execute()
            self.__SPREADSHEET_ID = spreadsheet['spreadsheetId']
            print("-Criando cabeçalho")
            self.salvar_senha('Local', 'Login', 'Senha')
            with open('./userbank.pickle', 'xb') as file:
                pickle.dump(self.__SPREADSHEET_ID, file)

    @property
    def service(self):
        return self.__service

    @property
    def spreadsheet_id(self):
        return self.__SPREADSHEET_ID

    @spreadsheet_id.setter
    def spreadsheet_id (self, new_spreadsheet_id):
        self.__init__(new_spreadsheet_id)

    def salvar_senha(self, local, login, senha):
        # Call the Sheets API
        values = [
            [
                local, login, senha
            ],
        ]
        body = {
            'values': values
        }
        self.__service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A:C',
                valueInputOption='RAW',
                body=body).execute()

    def ler_senhas (self):
        result = self.__service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range='Sheet1!A:C').execute()
        return result.get('values', [])

    def atualiza_senha (self, senhas):

        values = senhas
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range="Sheet1!A:C",
            valueInputOption="RAW", body=body).execute()
