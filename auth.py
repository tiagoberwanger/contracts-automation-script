import os.path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth import default

# If modifying these scopes, delete the file token.json
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.compose'
]

load_dotenv()

# CLIENT_CONFIG = {'installed': {
#     'client_id': os.getenv('GOOGLE_CLIENT_ID'),
#     'project_id': os.getenv('GOOGLE_PROJECT_ID'),
#     'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
#     'token_uri': "https://oauth2.googleapis.com/token",
#     'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
#     'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
#     'redirect_uris': [
#         os.getenv('GOOGLE_URIS')
#     ],
# }}

documento_id_com_dados_inquilinos = "1UzHWKA-qZTEfPDXs1l4o7FUp3BuI-MZcU3aEqYYJCbo"


# def get_authenticated_service(service_name: str, version: str):
#     """Shows basic usage of the API."""
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json()) 
#     try:
#         service = build(service_name, version, credentials=creds)
#         return service
#     except HttpError as error:
#         return f"Ocorreu um erro na autenticação: {error}"


def get_authenticated_service(service_name: str, version: str):
    creds, _ = default(scopes=SCOPES)
    try:
        service = build(service_name, version, credentials=creds)
        return service
    except HttpError as error:
        return f"Ocorreu um erro na autenticação: {error}"
    