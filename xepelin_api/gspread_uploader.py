
import gspread
import os
from gspread_dataframe import set_with_dataframe
from loguru import logger
from dotenv import load_dotenv
import json

load_dotenv()


def upload_dataframe_to_google_spread_sheet(df):
    logger.info('entering')
    credentials = json.loads(os.environ.get("GCLOUD_CREDENTIALS"))
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
    
    