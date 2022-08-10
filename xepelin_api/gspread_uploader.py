
import gspread
import os
from gspread_dataframe import set_with_dataframe
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def upload_dataframe_to_google_spread_sheet(df):
    logger.info('entering')
    credentials = { 
    "type": os.environ.get("GSPREAD_TYPE"),
    "project_id": os.environ.get("GSPREAD_PROJECT_ID"),
    "private_key_id" : os.environ.get("GSPREAD_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("GSPREAD_PRIVATE_KEY").replace("'\\'", "'\'"),
    "client_email": os.environ.get("GSPREAD_CLIENT_EMAIL"),
    "client_id": os.environ.get("GSPREAD_CLIENT_ID"),
    "auth_uri": os.environ.get("GSPREAD_AUTH_URI"),
    "token_uri": os.environ.get("GSPREAD_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("GSPREAD_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("GSPREAD_CLIENT_X509_CERT_URL")}
    logger.info(credentials)
    try:
        gc = gspread.service_account_from_dict(credentials)
        logger.info(gc)
        sh = gc.open_by_key(os.environ.get("SPREADSHEET_KEY"))
        logger.info(sh)
        worksheet = sh.get_worksheet(0)
        logger.info(worksheet)
        worksheet.clear()
        set_with_dataframe(worksheet, df)
    except Exception as e:
        logger.info(e)
        logger.info('Error')        