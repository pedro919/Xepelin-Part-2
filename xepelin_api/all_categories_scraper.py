from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from gspread_uploader import upload_posts_to_google_spread_sheet
import os

load_dotenv()


def load_all_posts(driver):
    #category = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[3]/div/h1').text
    load_more_posts = True
    while load_more_posts:
        try:
            button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[3]/div/div[2]/button')
        except exceptions.NoSuchElementException:
            load_more_posts = False
        else:        
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)


def get_posts_information(driver, category_name):
    posts_list = []
    for post in driver.find_elements(By.CLASS_NAME, 'BlogArticlesPagination_articleNormal__wvB1u'):
        title = post.find_element(By.XPATH, './/div[2]/div[1]/h3').text
        author = post.find_element(By.XPATH, './/div[3]/div/div[2]/div').text
        release_date = post.find_element(By.XPATH, './/div[2]/p').text
        post_dict = {'Titular': title, 'Categoría': category_name, 'Autor': author, 'Fecha de publicación': release_date}
        posts_list.append(post_dict)
    return posts_list


def all_categories_scraper_function():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("CHROME_BINARY_PATH")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"), chrome_options=chrome_options)
    driver.get('https://xepelin.com/blog')
    child_number= 5
    continue_with_next_category = True
    all_posts_list = []

    while continue_with_next_category:
        try:
            category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#__next > div > main > div:nth-child({str(child_number)})')))

        except exceptions.TimeoutException:
            continue_with_next_category=False
        
        else:
            button = WebDriverWait(category, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#__next > div > main > div:nth-child({str(child_number)}) > div > div.grid.mt-9.md\:mt-14 > a')))
            driver.execute_script("arguments[0].click();", button)
            category_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[3]/div/h1'))).text
            load_all_posts(driver)
            posts_list = get_posts_information(driver, category_name)
            all_posts_list += posts_list
            driver.back()
            child_number += 1

    driver.close()
    upload_posts_to_google_spread_sheet(all_posts_list)