
import gspread
import os
from gspread_dataframe import set_with_dataframe
import json
import pandas as pd


def upload_posts_to_google_spread_sheet(posts_list):
    df = pd.DataFrame(posts_list)
    credentials = json.loads(os.environ.get("GCLOUD_CREDENTIALS"))
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key(os.environ.get("SPREADSHEET_KEY"))
    worksheet = sh.get_worksheet(0)
    worksheet.clear()
    set_with_dataframe(worksheet, df)
    