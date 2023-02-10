from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pickle
import sys
import requests
import time
from bs4 import BeautifulSoup
import asyncio
from telethon import *
from telethon import sync
import os
from lxml import html
from configparser import ConfigParser

# Read config.ini
config = ConfigParser()
config.read('config.ini')

api_id = config.getint('Telegram_bot', 'api_id')
api_hash = config.get('Telegram_bot', 'api_hash')
bot_token = config.get('Telegram_bot', 'bot_token')
chat = config.getint('Telegram_bot', 'chat')
username = config.get('Login', 'username')
password = config.get('Login', 'password')

bot = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

total_id = []
all_id = []
printed_id = []

options = webdriver.ChromeOptions()
prefs={"download.default_directory":f"{os.getcwd()}\down"};
options.add_experimental_option("prefs",prefs);
ser = Service("driver/chromedriver.exe")
browser = webdriver.Chrome(service=ser ,options=options)

async def sel_login():
    browser.maximize_window()
    browser.implicitly_wait(5)
    browser.get("https://daring.uin-suka.ac.id");
    browser.delete_cookie("PHPSESSID")
    old_cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in old_cookies:
        browser.add_cookie(cookie)
    browser.get("https://daring.uin-suka.ac.id/dashboard")
    for i in range(len(old_cookies)):
        if old_cookies[i]["name"] == "PHPSESSID":
            cookiez = old_cookies[i]["value"]
    time.sleep(5)
    global ps
    ps = browser.page_source
    try :
        WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
            )
        nama = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
        await bot.send_message(chat, f"Berhasil Login dengan cookies yang sudah ada !\n `PHPSESSID` : `{cookiez}`\n dengan nama : **{nama.text}**")
    except:
        await bot.send_message(chat, "Tidak bisa login dengan cookies yang ada, mencoba mengambil cookies baru")
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
            await bot.send_message(chat, f"cookies berhasil didapatkan !\n `PHPSESSID` : `{cookiez}` \n dengan nama : **{nama.text}**")
            pickle.dump(new_cookies, open("cookies.pkl","wb"))
        except Exception as e :
            print(e)

    


def take_ss(browser, full_id):
    element = browser.find_element(By.ID, full_id)
    browser.execute_script("arguments[0].scrollIntoView(true);", element)
    element2 = browser.find_element(By.ID, full_id)
    location = element2.location
    size = element2.size
    num_id = num_id = full_id.replace("dv-progres-sts-","") 
    names = "pic/" + num_id + ".png"
    name = "pic/" + num_id + "-2.png"
    browser.save_screenshot(names)

    x = location['x']
    y = location['y']
    y2 = 1
    w = size['width']
    h = size['height']
    width = x + w
    height = y2 + h

    im = Image.open(names)
    im = im.crop((int(x), int(1), int(width), int(h)))
    im.save(name)
    return(name)

def cek_id():
    WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
        )
    ids = browser.find_elements(By.XPATH,'//*[starts-with(@id, "dv-progres-sts")]')
    for ii in range(len(ids)):
        full_id = ids[ii].get_attribute('id')
        all_id.append(full_id)

def cek_jenis_all():
    for full_id in all_id:
        print(full_id)
        total_id.append(full_id)
        pickle.dump(total_id, open("all_id.p", "wb"))
        jenis = cek_jenis(full_id)
        num_id = full_id.replace("dv-progres-sts-","")
        if full_id != printed_id:
            print(jenis)
            if jenis=="Tugas":
                pic_name = take_ss(browser, full_id)
                loop.run_until_complete(tugasbot(full_id, pic_name))
            elif jenis=="Diskusi":
                pic_name = take_ss(browser, full_id)
                loop.run_until_complete(diskusibot(full_id, pic_name))
            else:
                print(jenis)
                #auto_hadir(num_id)
        else:
            print("Tidak ada update tugas")

def cek_jenis(full_id):
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    bs_id = full_id.replace("dv-progres-sts-","dv-jurnalperkuliahan-")
    main = soup.find("div", {"id": str(full_id)})
    try:
        text_main = main.get_text(" | ", strip = True ).split(" | ")
    except:
        print("using sleep") 
        browser.get((browser.current_url))
        time.sleep(10)
        text_main = main.get_text(" | ", strip = True ).split(" | ")
    jenis = text_main[0]
    if jenis == "Forum":
        return jenis
    elif jenis == "Tugas":
        return jenis
    else:
        return (text_main[1])

def auto_hadir(num_id):
    combox = str("textarea" + num_id)
    combutt = str("btn-sv-reply-comment-" + num_id)
    root = html.fromstring(browser.page_source)
    tree = root.getroottree()
    elem = root.xpath(f'//*[@id="dv-progres-sts-{num_id}"]')
    for e in elem:
        z = tree.getpath(e)
    button_xpath = z.replace("/div[1]","/div[3]/div[2]/div[1]/form/input[2]")
    try:
       browser.find_element(By.ID, combox).send_keys("hadir");
       browser.find_element(By.XPATH,button_xpath).click() 
    except Exception as e:
        print(e)
        pass

def scrape(ps):
    global soup
    soup = BeautifulSoup(ps, 'html.parser')

    # try :
    fall_ids = pickle.load(open("all_id.p", "rb"))
    for i in fall_ids:
        total_id.append(i)
    fprinted_ids = pickle.load(open("printed_id.p", "rb"))
    for i in fprinted_ids:
        printed_id.append(i)
    # except:
    #     pass

async def tugasbot(full_id, pic_name):
    # pilih id yang mau dipakai
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    itext_b = len(text_b)
    Node = itext_b - 8
    desc =[]
    for i in text_b[:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)
    capt = f"""**jenis : **{text_a[0]}
**Jurusan :**{text_a[2]}
**Matkul :**{text_a[3]}
**Dosen :**{text_a[4]}
**Deskripsi :**{desc2}
**Waktu mulai**{text_b[(itext_b-4)]}
**Waktu mulai**{text_b[(itext_b-2)]}
"""
    await bot.send_file(chat, pic_name, caption=capt)
    
    # download file yang ada pada post
    try:
        file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
        file_name = file.text
        try:
            filez = await bot.upload_file(f'down/{file_name}')
            await bot.send_file(chat, filez)
        except:
            file.click()
            time.sleep(5)
            filez = await bot.upload_file(f'down/{file_name}')
            await bot.send_file(chat, filez)
    except:
        await bot.send_message(chat, "No File Attached")    
    printed_id.append(full_id)
    pickle.dump(printed_id, open("printed_id.p", "wb"))

async def diskusibot(full_id, pic_name):
    # ambil text
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    if total_file > 0 :
        total_file2 = total_file * 2 + 1
        Node = itext_b - 11 - total_file2
    else:
        Node = itext_b - 11
    
    ## untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
    desc =[]
    for i in text_b[6:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)
    
    ## bot caption maker
    capt = f"""**Jenis :** {text_a[1]}
**Jurusan :** {text_a[3]}
**Matkul :  **{text_a[4]}
**Dosen : **{text_a[5]}
**Indikator Kemampuan : **{text_b[1]}
**Materi Perkuliahan : **{text_b[3]}
**Bentuk Pembelajaran : **{text_b[5]}
**Deskripsi : **{desc2}
**Waktu mulai  **{text_b[(itext_b-7)]}
**Waktu selesai  **{text_b[(itext_b-5)]}
"""
    await bot.send_file(chat, pic_name, caption=capt)
    # download file yang ada pada post
    total_file = browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p')
    if len(total_file) == 1:
        try:
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
            file_name = file.text
            print(file_name)
        except:
            raise Exception
    else :
        for i in range(1, len(total_file)+1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            file_name = file.text
            clickable.click()
            time.sleep(2)
            file_upload = await bot.upload_file(f'down/{file_name}')
            await bot.send_file(chat, file_upload)

def main():
    global loop
    loop = asyncio.new_event_loop() # untuk menjalankan async
    loop.run_until_complete(sel_login()) #login
    scrape(browser.page_source) #persiapan beautiful soup
    cek_id() #mengambil data yang ada pada page
    cek_jenis_all() #menganalisis tiap data
    bot.run_until_disconnected

main()
