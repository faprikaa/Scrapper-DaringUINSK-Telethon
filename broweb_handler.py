from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from bs4 import BeautifulSoup
import pickle, os, datetime, pytz
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
down_path = thisfolder + r"//down"

def init_browser():
    options = webdriver.ChromeOptions()
    prefs={"download.default_directory": "/root/daring3/down", "download.directory_upgrade": True}
    options.add_experimental_option("prefs",prefs )
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
    browser = webdriver.Chrome(service=ser ,options=options)
    browser.maximize_window()
    return browser

async def login():
    browser.get("https://daring.uin-suka.ac.id")
    try :
        browser.delete_cookie("PHPSESSID")
        old_cookies = pickle.load(open("cookies.txt", "rb"))
        for i in range(len(old_cookies)):
            browser.add_cookie(old_cookies[i])
        browser.get("https://daring.uin-suka.ac.id")
        WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
            )
        new_cookies = browser.get_cookies() 
        for i in range(len(new_cookies)):
            if new_cookies[i]["name"] == "PHPSESSID":
                cookiez = new_cookies[i]["value"]
                try:
                    expired = datetime.datetime.fromtimestamp(new_cookies[i]["expiry"], time_jakarta)
                    nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
                    await send_msg(f"Berhasil Login dengan cookies yang sudah ada !\n`PHPSESSID` : `{cookiez}`,\nnama : **{nama.text}**,\nexpired : **{expired}** ")
                except:
                    nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
                    await send_msg(f"Berhasil Login dengan cookies yang sudah ada !\n`PHPSESSID` : `{cookiez}`,\nnama : **{nama.text}**")
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
                try:
                    expired = datetime.datetime.fromtimestamp(new_cookies[i]["expiry"], time_jakarta)
                except:
                    pass
            nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            await send_msg(f"cookies berhasil didapatkan !\n`PHPSESSID` : `{cookiez}` \nnama : **{nama.text}**,\nexpired : **{expired}**")
            pickle.dump(new_cookies, open("cookies.txt","wb"))
        except :
            await send_msg(f"An error occured, {traceback.format_exc()}")
    return browser

async def cookies_login(cookies):
    try:
        # await send_msg(f"Mencoba login dengan cookies yang diberikan `{cookies}`")
        browser.get("https://daring.uin-suka.ac.id")
        get_cookies =      {
        "domain": "daring.uin-suka.ac.id",
        "name": "PHPSESSID",
        "path": "/",
        "value": cookies
    }
        browser.delete_cookie("PHPSESSID")
        browser.add_cookie(get_cookies)
        browser.get("https://daring.uin-suka.ac.id")
        print(browser.get_cookies())
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
        except TimeoutException:
            await send_msg(f"Gagal login dengan cookies yang diberikan\nCek lagi cookies yang diberikan !")
        else :
            new_cookies = browser.get_cookies()
            print(new_cookies)
            for i in range(len(new_cookies)):
                if new_cookies[i]["name"] == "PHPSESSID":
                    cookiez = new_cookies[i]["value"]
            pickle.dump(new_cookies, open("cookies.txt","wb"))
            nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
            await send_msg(f"Berhasil login dengan !\n `PHPSESSID` : `{cookiez}` \nnama : **{nama.text}**")
    except:
        await send_msg(f"An error occured, {traceback.format_exc()}")


def cek_id():
    all_id = [ ]
    try:
        WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
            )
    except TimeoutError:
        browser.get("https://daring.uin-suka.ac.id")
    ids = browser.find_elements(By.XPATH,'//*[starts-with(@id, "dv-progres-sts")]')
    for ii in range(len(ids)):
        full_id = ids[ii].get_attribute('id')
        all_id.append(full_id)
    return all_id

def status_checker(full_id):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    try:
        status = main.attrs["class"][2]
        return status
    except:
        return "no-status-found"

def komen():
    arr_id =  cek_id()
    for full_id in arr_id:
        num_id = full_id.replace("dv-progres-sts-","")
        print(num_id)
        ahref = browser.find_element(By.XPATH, f'//*[@id={num_id}]')
        ahref.click()

    nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b").text
    cnama = browser.find_elements(By.XPATH, f"//div[contains(text()={nama})]")
    for i in cnama:
        print(i.outer_html)

browser = init_browser()