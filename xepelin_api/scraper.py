from selenium import webdriver, common
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

def blog_scraper(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("CHROME_BINARY_PATH")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)
    category = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[3]/div/h1').text
    load_more_posts = True

    while load_more_posts:
        try:
            button = driver.find_element('xpath', '//*[@id="__next"]/div/main/div[3]/div/div[2]/button')
        except common.exceptions.NoSuchElementException:
            load_more_posts = False
        else:        
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
    
    posts_list = []
    for post in driver.find_elements(By.CLASS_NAME, 'BlogArticlesPagination_articleNormal__wvB1u'):
        title = post.find_element(By.XPATH, './/div[2]/div[1]/h3').text
        author = post.find_element(By.XPATH, './/div[3]/div/div[2]/div').text
        release_date = post.find_element(By.XPATH, './/div[2]/p').text
        post_dict = {'Titular': title, 'Categoría': category, 'Autor': author, 'Fecha de publicación': release_date}
        posts_list.append(post_dict)

    df = pd.DataFrame(posts_list)
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
