import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from util.config import DOWNLOAD_PATH, OS_TYPE

thisfolder = os.getcwd()
down_path = os.path.join(thisfolder, DOWNLOAD_PATH)


def init_browser():
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": down_path,
             "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)
    if OS_TYPE == "Linux":
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
    else:
        ser = Service("driver/chromedriver.exe")
        driver = webdriver.Chrome(service=ser, options=options)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    return driver


browser = init_browser()
