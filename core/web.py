import traceback

from selenium.common import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from core.bot import bot
from core.browser import browser
from core.classes.Post import Post
from util.config import CHAT_ID, USERNAME, PASSWORD
from util.cookies import load_cookies_from_file, insert_cookies_to_browser, insert_cookies_to_file
from util.web_utils import cek_jenis, get_nama_mhs
from utils import html_id_to_post_id


async def login():
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
Nama : {get_nama_mhs()}
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
Nama : {get_nama_mhs()}
            """
            await bot.delete_messages(entity=CHAT_ID, message_ids=msg1.id)

        except NoSuchElementException:
            pass
        except:
            await bot.send_message(CHAT_ID, f"An error occured, {traceback.format_exc()}")
        finally:
            await bot.send_message(CHAT_ID, msg)

    else:
        await bot.send_message(CHAT_ID, msg)


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


async def force_cek_jenis_all(all_id):
    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except:
        await bot.send_message(CHAT_ID, "Cookies habis silahkan login ulang")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    for html_id in all_id:
        try:
            post = Post(html_id_to_post_id(html_id))
            await post.send()
        except Exception as e:
            await bot.send_message(CHAT_ID, f"An error occured, {traceback.format_exc()}")
        # await auto_hadir(full_id)
    pass


def alert_checker():
    try:
        browser.switch_to.alert
    except:
        pass
    else:
        login()
