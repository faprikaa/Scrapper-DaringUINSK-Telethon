from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from bs4 import BeautifulSoup
import pickle
import os
import datetime
import pytz
import json
from configparser import ConfigParser
import traceback
import bot_handler

send_msg = bot_handler.send_msg
send_file = bot_handler.send_file

config = ConfigParser()
config.read('config.ini')
username = config.get('Login', 'username')
password = config.get('Login', 'password')
OS_type = config.get('Driver', 'OS')

time_jakarta = pytz.timezone('Asia/Jakarta')
thisfolder = os.getcwd()
down_path = os.path.join(thisfolder, str(config.get('Driver', 'download_path')))


def init_browser():
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": down_path,
             "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)
    if OS_type == "Linux":
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        ser = Service("/usr/bin/chromedriver")
    else:
        ser = Service("driver/chromedriver.exe")
    browser = webdriver.Chrome(service=ser, options=options)
    browser.set_window_size(1920, 1080)
    browser.maximize_window()
    return browser


async def login():
    try:
        browser.get("https://daring.uin-suka.ac.id")
    except UnexpectedAlertPresentException:
        a = browser.switch_to.alert()
        a.accept()
        browser.get("https://daring.uin-suka.ac.id")
    try:
        browser.delete_cookie("PHPSESSID")
        openfile = open("cookies.txt", "r+")
        old_cookies = json.load(openfile)
        for i in range(len(old_cookies)):
            browser.add_cookie(old_cookies[i])
            if old_cookies[i]["name"] == "PHPSESSID":
                cookiez = old_cookies[i]["value"]
                expired = datetime.datetime.fromtimestamp(
                    old_cookies[i]["expiry"], time_jakarta)
        browser.get("https://daring.uin-suka.ac.id")
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
        )
        nama = browser.find_element(
            By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
        await send_msg(f"Berhasil Login dengan cookies yang sudah ada !\n`PHPSESSID` : `{cookiez}`,\nnama : **{nama.text}**,\nexpired : **{expired}** ")
    except:
        await send_msg("Tidak bisa login dengan cookies yang ada, mencoba mengambil cookies baru")
        try:
            browser.find_element(By.ID, "username").send_keys(username)
            browser.find_element(By.ID, "password").send_keys(password)
            browser.find_element(By.CLASS_NAME, "btn-uin").click()
            browser.implicitly_wait(5)
            new_cookies = browser.get_cookies()
            for i in range(len(new_cookies)):
                if new_cookies[i]["name"] == "PHPSESSID":
                    cookiez = new_cookies[i]["value"]
                    expired = datetime.datetime.fromtimestamp(
                        new_cookies[i]["expiry"], time_jakarta)
            nama = browser.find_element(
                By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            await send_msg(f"cookies berhasil didapatkan !\n`PHPSESSID` : `{cookiez}` \nnama : **{nama.text}**,\nexpired : **{expired}**")
            openfile = open("cookies.txt", "w+")
            json_cookies = json.dumps(new_cookies, indent=4)
            openfile.writelines(json_cookies)
        except NoSuchElementException:
            new_cookies = browser.get_cookies()
            for i in range(len(new_cookies)):
                if new_cookies[i]["name"] == "PHPSESSID":
                    cookiez = new_cookies[i]["value"]
                    expired = datetime.datetime.fromtimestamp(
                        new_cookies[i]["expiry"], time_jakarta)
            nama = browser.find_element(
                By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            await send_msg(f"cookies berhasil didapatkan !\n`PHPSESSID` : `{cookiez}` \nnama : **{nama.text}**,\nexpired : **{expired}**")
            pass
        except:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    return browser


async def cookies_login(cookies):
    try:
        browser.delete_cookie("PHPSESSID")
        await send_msg(f"Mencoba login dengan cookies yang diberikan `{cookies}`")
        browser.get("https://daring.uin-suka.ac.id")
        openfile = open("cookies.txt", "r+")
        old_cookies = json.load(openfile)
        for i in range(len(old_cookies)):
            if old_cookies[i]["name"] == "PHPSESSID":
                old_cookies[i]["value"] = cookies
            browser.add_cookie(old_cookies[i])
        browser.get("https://daring.uin-suka.ac.id")
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
        except TimeoutException:
            await send_msg("Gagal login dengan cookies yang diberikan")
        else:
            new_cookies = browser.get_cookies()
            for i in range(len(new_cookies)):
                if new_cookies[i]["name"] == "PHPSESSID":
                    cookiez = new_cookies[i]["value"]
                    expired = datetime.datetime.fromtimestamp(
                        old_cookies[i]["expiry"], time_jakarta)
            pickle.dump(new_cookies, open("cookies.txt", "wb"))
            nama = browser.find_element(
                By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            await send_msg(f"Berhasil login dengan !\n `PHPSESSID` : `{cookiez}` \nnama : **{nama.text}**,\nexpired : **{expired}**")
    except:
        await send_msg(f"An error occured, {traceback.format_exc()}")


async def cek_id():
    all_id = []
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
        )
    except TimeoutException:
        browser.get("https://daring.uin-suka.ac.id")
        await login()
    except UnexpectedAlertPresentException:
        browser.get("https://daring.uin-suka.ac.id")
        await login()
    ids = browser.find_elements(
        By.XPATH, '//*[starts-with(@id, "dv-progres-sts")]')
    for ii in range(len(ids)):
        full_id = ids[ii].get_attribute('id')
        all_id.append(full_id)
    return all_id


def get_cookies():
    alert_checker()
    new_cookies = browser.get_cookies()
    for i in range(len(new_cookies)):
        if new_cookies[i]["name"] == "PHPSESSID":
            cookiez = new_cookies[i]["value"]
            return cookiez
    return None


def alert_checker():
    try:
        browser.switch_to.alert()
    except:
        pass
    else:
        login()


def status_checker(full_id):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    try:
        status = main.attrs["class"][2]
        return status
    except:
        return "no-status-found"


browser = init_browser()
