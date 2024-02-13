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
from util.config import DOWNLOAD_PATH, OS_TYPE, TIMEZONE, CHAT_ID, USERNAME, PASSWORD
from core.bot import bot

thisfolder = os.getcwd()
down_path = os.path.join(thisfolder, DOWNLOAD_PATH)

async def login():
    php_cookie = ""
    exp_cookie = ""
    msg = ""
    try:
        browser.get("https://daring.uin-suka.ac.id")
    except UnexpectedAlertPresentException:
        a = browser.switch_to.alert
        a.accept()
        browser.get("https://daring.uin-suka.ac.id")
    try:
        browser.delete_cookie("PHPSESSID")
        openfile = open("cookies.txt", "r+")
        old_cookies = json.load(openfile)
        for cookie in old_cookies:
            browser.add_cookie(cookie)
            if cookie["name"] == "PHPSESSID":
                php_cookie = cookie["value"]
                exp_cookie = datetime.datetime.fromtimestamp(cookie["expiry"], TIMEZONE)

        browser.get("https://daring.uin-suka.ac.id")
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
        )
        nama = browser.find_element(
            By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
        msg = f"""
        Berhasil login dengan cookies yang ada !
        `PHPSESSID` : {php_cookie}
        `EXPIRY` : {exp_cookie}
        Nama : {nama}
        """
        openfile.close()

    except:
        msg1 = await bot.send_message(CHAT_ID, "Tidak bisa login dengan cookies yang ada, mencoba mengambil cookies baru")
        try:
            browser.find_element(By.ID, "username").send_keys(USERNAME)
            browser.find_element(By.ID, "password").send_keys(PASSWORD)
            browser.find_element(By.CLASS_NAME, "btn-uin").click()
            browser.implicitly_wait(5)
            new_cookies = browser.get_cookies()
            for cookie in new_cookies:
                browser.add_cookie(cookie)
                if cookie["name"] == "PHPSESSID":
                    php_cookie = cookie["value"]
                    exp_cookie = datetime.datetime.fromtimestamp(cookie["expiry"], TIMEZONE)
            nama = browser.find_element(
                By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            msg = f"""
            Berhasil login dengan cookies yang ada !
            `PHPSESSID` : {php_cookie}
            `EXPIRY` : {exp_cookie}
            Nama : {nama}
            """
            openfile = open("cookies.txt", "w+")
            json_cookies = json.dumps(new_cookies, indent=4)
            openfile.writelines(json_cookies)
            openfile.close()

        except NoSuchElementException:
            new_cookies = browser.get_cookies()
            for cookie in new_cookies:
                browser.add_cookie(cookie)
                if cookie["name"] == "PHPSESSID":
                    php_cookie = cookie["value"]
                    exp_cookie = datetime.datetime.fromtimestamp(cookie["expiry"], TIMEZONE)
            nama = browser.find_element(
                By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            msg = f"""
            Berhasil login dengan cookies yang ada !
            `PHPSESSID` : {php_cookie}
            `EXPIRY` : {exp_cookie}
            Nama : {nama}
            """
            pass
        except:
            await bot.send_message(CHAT_ID, f"An error occured, {traceback.format_exc()}")
        else:
            await bot.delete_messages(msg1)

    await bot.send_message(CHAT_ID, msg)
    return browser


async def cookies_login(cookies):
    try:
        browser.delete_cookie("PHPSESSID")
        await bot.send_message(CHAT_ID, f"Mencoba login dengan cookies yang diberikan `{cookies}`")
        browser.get("https://daring.uin-suka.ac.id")
        openfile = open("cookies.txt", "r+")
        old_cookies = json.load(openfile)
        for cookie in old_cookies:
            if cookie["name"] == "PHPSESSID":
                cookie["value"] = cookies
            browser.add_cookie(cookie)
        browser.get("https://daring.uin-suka.ac.id")
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
        except TimeoutException:
            await bot.send_message(CHAT_ID, "Gagal login dengan cookies yang diberikan")
        else:
            new_cookies = browser.get_cookies()
            for cookie in new_cookies:
                browser.add_cookie(cookie)
                if cookie["name"] == "PHPSESSID":
                    php_cookie = cookie["value"]
                    exp_cookie = datetime.datetime.fromtimestamp(cookie["expiry"], TIMEZONE)
            nama = browser.find_element(
                By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            msg = f"""
            Berhasil login dengan cookies yang ada !
            `PHPSESSID` : {php_cookie}
            `EXPIRY` : {exp_cookie}
            Nama : {nama}
            """
            await bot.send_message(CHAT_ID, msg)
    except:
        await bot.send_message(CHAT_ID ,f"An error occured, {traceback.format_exc()}")


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
    for id in ids:
        html_id = id.get_attribute('id')
        all_id.append(html_id)
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
        browser.switch_to.alert
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


# browser = init_browser()
