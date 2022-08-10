from selenium import webdriver
import os


def blog_scraper():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("CHROME_BINARY_PATH")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"), chrome_options=chrome_options)
    driver.get("https://medium.com")
    print(driver.page_source)
    print("Finished!")
