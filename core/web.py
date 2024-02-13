import json
import traceback
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import UnexpectedAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from bot import bot
from util.config import TIMEZONE, CHAT_ID, USERNAME, PASSWORD
from util.cookies import load_cookies_from_file, insert_cookies_to_browser, insert_cookies_to_file, get_php_cookie


async def login(browser):
    php_cookie = ""
    exp_cookie = ""
    msg = ""

    try:
        browser.get("https://daring.uin-suka.ac.id")
    except UnexpectedAlertPresentException:
        a = browser.switch_to.alert
        a.accept()
        browser.get("https://daring.uin-suka.ac.id")

    try:  # login pake cookie yang ada
        browser.delete_cookie("PHPSESSID")
        saved_cookies = load_cookies_from_file()
        insert_cookies_to_browser(browser, saved_cookies)
        browser.get("https://daring.uin-suka.ac.id")
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
        )
        php_json_cookie = browser.get_cookie("PHPSESSID")
        php_cookie = php_json_cookie["value"]
        exp_cookie = php_json_cookie["expiry"]
        msg = f"""
        Berhasil login dengan cookies yang ada !
    `PHPSESSID` : `{php_cookie}`
    `EXPIRY` : `{exp_cookie}`
    Nama : {get_nama_mhs(browser)}
        """

    except Exception as e:  # login dengan username dan pw
        msg1 = await bot.send_message(
            CHAT_ID,
            "Tidak bisa login dengan cookies yang ada, mencoba mengambil cookies baru")

        try:
            browser.find_element(By.ID, "username").send_keys(USERNAME)
            browser.find_element(By.ID, "password").send_keys(PASSWORD)
            browser.find_element(By.CLASS_NAME, "btn-uin").click()
            browser.implicitly_wait(5)
            new_cookies = browser.get_cookies()
            insert_cookies_to_file(new_cookies)
            php_json_cookie = browser.get_cookie("PHPSESSID")
            php_cookie = php_json_cookie["value"]
            exp_cookie = php_json_cookie["expiry"]
            msg = f"""
            Berhasil login dengan username dan password !
        `PHPSESSID` : `{php_cookie}`
        `EXPIRY` : `{exp_cookie}`
        Nama : {get_nama_mhs(browser)}
            """

        except NoSuchElementException:
            pass
        except:
            await bot.send_message(CHAT_ID, f"An error occured, {traceback.format_exc()}")
        else:
            await bot.delete_messages(entity=msg1.entities,message_ids=msg1.id)
            await bot.send_message(CHAT_ID, msg)

    else:
        await bot.send_message(CHAT_ID, msg)


def get_nama_mhs(browser):
    nama = browser.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    return nama.text.strip()
