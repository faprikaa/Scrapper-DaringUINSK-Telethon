import json
import traceback

from selenium.common import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from core.bot import bot
from core.browser import browser
from core.classes.Post import Post
from util.config import CHAT_ID, USERNAME, PASSWORD
from util.cookies import load_cookies_from_file, insert_cookies_to_browser, insert_cookies_to_file
from util.web_utils import get_nama_mhs
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


async def load_saved_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

async def cek_jenis_all(all_id, force=False):
    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except NoSuchElementException:
        await bot.send_message(CHAT_ID, "Cookies expired. Please login again.")
        return

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))

    saved_data = await load_saved_data()
    new_ids = []

    for html_id in all_id:
        post_id = html_id_to_post_id(html_id)
        if post_id not in saved_data:
            new_ids.append(post_id)
    if len(new_ids) < 1:
        await bot.send_message(CHAT_ID, "Tidak ada postingan baru/")
    for post_id in new_ids:
        try:
            post = Post(post_id)
            await post.send()
            if force:
                saved_data[post_id] = post.to_json()
                save_data(saved_data)

        except Exception as e:
            await bot.send_message(CHAT_ID, f"An error occurred: {e}")
            # Optionally, log the error or handle it appropriately

        # await auto_hadir(full_id)  # Uncomment if needed


async def click_next():
    button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[12]/center/button")
    try:
        click = button.click()
        expected = len(await cek_id()) + 1
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="update"]/li[{expected}]')))
        return ("Tombol Perlihatkan Sebelumnya berhasil di klik kali !!")
    except UnexpectedAlertPresentException:
        return ("Cookies habis silahkan login ulang")
    except ElementNotInteractableException:
        return ("Please wait 10 seconds before send this command again")
    except:
        return (f"An error occured at next, {traceback.format_exc()}")



def alert_checker():
    try:
        browser.switch_to.alert
    except:
        pass
    else:
        login()
