import json
import traceback
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from core.bot import bot
from core.post import Tugas
from util.config import TIMEZONE, CHAT_ID, USERNAME, PASSWORD
from util.cookies import load_cookies_from_file, insert_cookies_to_browser, insert_cookies_to_file, get_php_cookie
from core.browser import browser
from utils import html_id_to_post_id


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

        except NoSuchElementException:
            pass
        except:
            await bot.send_message(CHAT_ID, f"An error occured, {traceback.format_exc()}")
        else:
            await bot.delete_messages(entity=msg1.entities, message_ids=msg1.id)
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
        jenis = cek_jenis(html_id)
        try:
            if jenis=="Tugas":
                # data = await tugasbot(full_id)
                tgs = Tugas(html_id_to_post_id(html_id))
                data = tgs.to_json()
                await tgs.send()
            # elif jenis=="Diskusi":
            #     data = await diskusibot(full_id)
            # elif jenis=="Meeting":
            #     data = await meetingbot(full_id)
            # elif jenis=="Forum":
            #     data = await forumbot(full_id)
            # elif jenis=="Materi":
            #     data = await materibot(full_id)
            # elif jenis=="Video":
            #     data = await videobot(full_id)
            # elif jenis=="Pengumuman":
            #     data = await pengumumanbot(full_id)
            else:
                pass
                # await send_msg(f"Unknown post type, {jenis}")
        except Exception as e:
            await bot.send_message(CHAT_ID, f"An error occured, {traceback.format_exc()}")
        # await auto_hadir(full_id)
    pass


def cek_jenis(html_id):
    # print(full_id)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    try:
        main = soup.find("div", {"id": str(html_id)})
    except:
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        main = soup.find("div", {"id": str(html_id)})

    try:
        text_main = main.get_text(" | ", strip=True).split(" | ")
    except AttributeError:
        return "err-1"
    except:
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        main2 = soup2.find("div", {"id": str(html_id)})
        text_main = main2.get_text(" | ", strip=True).split(" | ")

    jenis = text_main[0]
    if jenis == "Forum":
        return jenis
    elif jenis == "Tugas":
        return jenis
    elif jenis == "Materi":
        return jenis
    elif jenis == "Pengumuman":
        return jenis
    else:
        return (text_main[1])


def get_nama_mhs():
    nama = browser.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    return nama.text.strip()


def alert_checker():
    try:
        browser.switch_to.alert
    except:
        pass
    else:
        login()
