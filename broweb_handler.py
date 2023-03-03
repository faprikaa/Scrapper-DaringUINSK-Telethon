from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pickle, os
from configparser import ConfigParser
import traceback
import bot_handler

send_msg = bot_handler.send_msg
send_file = bot_handler.send_file

config = ConfigParser()
config.read('config.ini')
username = config.get('Login', 'username')
password = config.get('Login', 'password')
driver_path = config.get('Driver', 'driver_path')
jsonfile = config.get('Driver', 'json_filename')
OS_type = config.get('Driver', 'OS')

thisfolder = os.getcwd()
down_path = thisfolder + r"//down"

def init_browser():
    options = webdriver.ChromeOptions()
    prefs={"download.default_directory": "/root/daring3/down", "download.directory_upgrade": True}
    options.add_experimental_option("prefs",prefs )
    options.add_experimental_option("detach", True)
    if OS_type == "Linux":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        ser = Service("/usr/bin/chromedriver")
    else:
        ser = Service("driver/chromedriver.exe")
    global browser
    browser = webdriver.Chrome(service=ser ,options=options)
    browser.maximize_window()
    return browser

async def login():
    browser.get("https://daring.uin-suka.ac.id")
    try :
        browser.delete_cookie("PHPSESSID")
        old_cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in old_cookies:
            browser.add_cookie(cookie)
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        for i in range(len(old_cookies)):
            if old_cookies[i]["name"] == "PHPSESSID":
                cookiez = old_cookies[i]["value"]
        WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
            )
        nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
        await send_msg(f"Berhasil Login dengan cookies yang sudah ada !\n `PHPSESSID` : `{cookiez}`\n dengan nama : **{nama.text}**")
    except:
        await send_msg("Tidak bisa login dengan cookies yang ada, mencoba mengambil cookies baru")
        try:
            browser.find_element(By.ID, "username").send_keys(username)
            browser.find_element(By.ID, "password").send_keys(password)
            browser.find_element(By.CLASS_NAME,"btn-uin").click()
            browser.implicitly_wait(5)
            new_cookies = browser.get_cookies()
            for i in range(len(new_cookies)):
                if new_cookies[i]["name"] == "PHPSESSID":
                    cookiez = new_cookies[i]["value"]
            nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            await send_msg(f"cookies berhasil didapatkan !\n `PHPSESSID` : `{cookiez}` \n dengan nama : **{nama.text}**")
            pickle.dump(new_cookies, open("cookies.pkl","wb"))
        except :
            await send_msg(f"An error occured, {traceback.format_exc()}")

    browser.set_window_size(1280, 720)
    return browser

def cek_id(browser):
    all_id = [ ]
    WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
        )
    ids = browser.find_elements(By.XPATH,'//*[starts-with(@id, "dv-progres-sts")]')
    for ii in range(len(ids)):
        full_id = ids[ii].get_attribute('id')
        all_id.append(full_id)
    return all_id

def status_checker(browser, full_id):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    try:
        status = main.attrs["class"][2]
        return status
    except:
        return "no-status-found"
