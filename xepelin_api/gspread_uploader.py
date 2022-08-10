
import gspread
import os
from gspread_dataframe import set_with_dataframe

def upload_dataframe_to_google_spread_sheet(df):
    credentials = { 
    "type": os.getenv("GSPREAD_TYPE"),
    "project_id": os.getenv("GSPREAD_PROJECT_ID"),
    "private_key_id" : os.getenv("GSPREAD_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GSPREAD_PRIVATE_KEY"),
    "client_email": os.getenv("GSPREAD_CLIENT_EMAIL"),
    "client_id": os.getenv("GSPREAD_CLIENT_ID"),
    "auth_uri": os.getenv("GSPREAD_AUTH_URI"),
    "token_uri": os.getenv("GSPREAD_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GSPREAD_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GSPREAD_CLIENT_X509_CERT_URL")}
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key(os.getenv("SPREADSHEET_KEY"))
    worksheet = sh.get_worksheet(0)
    worksheet.clear()
    set_with_dataframe(worksheet, df)