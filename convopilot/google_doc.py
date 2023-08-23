import pickle
import os.path
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDocWriter(object):
    def __init__(self, name, folder):
        self.creds = self._init_creds()
        self.document = self.create_doc(name, folder)
        print(
            f"Created google doc at https://docs.google.com/document/d/{self.document['documentId']}/edit")

    def _init_creds(self):
        credentials_text = os.environ.get("GOOGLE_DOC_CREDENTIALS")
        credentials = json.loads(credentials_text)
        # Load the credentials
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no valid credentials available, prompt the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    credentials,
                    ['https://www.googleapis.com/auth/documents',
                     'https://www.googleapis.com/auth/drive',
                     'https://www.googleapis.com/auth/drive.file'])
                creds = flow.run_local_server(port=0)
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
        return creds

    def create_doc(self, title, folder_id):
        service = build('docs', 'v1', credentials=self.creds)

        document = service.documents().create(body={'title': title}).execute()

        if folder_id == "":
            return document

        drive_service = build('drive', 'v3', credentials=self.creds)

        file_id = document['documentId']
        drive_service.files().update(fileId=file_id, addParents=folder_id,
                                     fields='id, parents').execute()

        return document

    def insert_paragraph_front(self, text, paragraph_style='NORMAL_TEXT'):
        service = build('docs', 'v1', credentials=self.creds)

        paragraph = text + "\n"
        start_index = 1
        end_index = start_index + len(paragraph)
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': start_index,
                    },
                    'text': paragraph
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': start_index,
                        'endIndex': end_index
                    },
                    'paragraphStyle': {
                        'namedStyleType': paragraph_style
                    },
                    'fields': 'namedStyleType'
                }
            }
        ]
        try:
            result = service.documents().batchUpdate(
                documentId=self.document['documentId'], body={'requests': requests}).execute()
            return result
        except HttpError as error:
            print(f'An error occurred: {error}')

    def __del__(self):
        print(
            f"Created google doc at https://docs.google.com/document/d/{self.document['documentId']}/edit")
