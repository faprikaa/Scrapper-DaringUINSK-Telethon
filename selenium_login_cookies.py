from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pickle
import json
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
browser = webdriver.Chrome(executable_path= "driver/chromedriver.exe",options=options)

async def sel_login():
    browser.maximize_window()
    browser.implicitly_wait(5)
    browser.get("https://daring.uin-suka.ac.id");
    browser.delete_cookie("PHPSESSID")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get("https://daring.uin-suka.ac.id/dashboard");
    cookiez = cookies[2].get('value')
    time.sleep(5)
    ps = browser.page_source
    try :
        WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
            )
    except:
        await bot.send_message(chat, "tidak bisa login dengan cookies yang ada, mencoba mengambil cookies baru")
        try:
            browser.find_element(By.ID, "username").send_keys(username);
            browser.find_element(By.ID, "password").send_keys(password);
            browser.find_element(By.CLASS_NAME,"btn-uin").click();
            browser.implicitly_wait(5)
            await bot.send_message(chat, f"cookies berhasil didapatkan !\n PHPSESSID : {cookiez}")
            pickle.dump(browser.get_cookies() , open("cookies.pkl","wb"))
        except Exception as e :
            print(e)
    finally:
        await bot.send_message(chat, "Berhasil login !")


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

# page_source = browser.page_source
# cookiez = {'PHPSESSID': cookie.get('value')}
# response = s.get('https://daring.uin-suka.ac.id/', cookies=cookiez, headers=headers)
# soup = BeautifulSoup(page_source, 'lxml')
# tugas(page_source,cookiez,"dv-progres-sts-194746")

def cek_id():
    WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
        )
    ids = browser.find_element(By.XPATH,'//*[@id]')
    for ii in ids:
        full_id = ii.get_attribute('id')
        if full_id.startswith("dv-progres-sts"):
            num_id = full_id.replace("dv-progres-sts-","") 
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
    print(main.text)
    #main = soup.find_all('div')
    #print(bs_id)
    try:
        text_main = main.get_text(" | ", strip = True ).split(" | ")
    except:
        print("using sleep") 
        print(main)
        time.sleep(10)
        text_main = main.get_text(" | ", strip = True ).split(" | ")
    jenis = text_main[0]
    if jenis == "Forum":
        return jenis
    else :
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

def main():
    global loop
    loop = asyncio.get_event_loop() # untuk menjalankan async
    loop.run_until_complete(sel_login()) #login
    scrape(browser.page_source) #persiapan beautiful soup
    cek_id() #mengambil data yang ada pada page
    cek_jenis_all() #menganalisis tiap data

async def diskusi(full_id):
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")

    ## untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
    itext_b = len(text_b)
    Node = itext_b - 11
    desc =[]
    for i in text_b[6:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)
    ##

    capt = f"""**jenis : {text_a[0]}
    jurusan : {text_a[3]}
    matkul :  {text_a[4]}
    dosen : {text_a[5]}
    Indikator Kemampuan : {text_b[1]}
    Materi Perkuliahan : {text_b[3]}
    Bentuk Pembelajaran : {text_b[5]}
    Deskripsi : {desc2}
    waktu mulai  {text_b[(itext_b-7)]}
    waktu selesai  {text_b[(itext_b-5)]}
    **"""
    print(capt)
    # download file yang ada pada post
    try:
        file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
        file_name = file.text
        print(file_name)
    except:
        print("No file attached")

async def tugas(full_id):
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    print("jenis : " + text_a[0] + text_a[1])
    print("jurusan : " + text_a[2])
    print("matkul : " + text_a[3])
    print("dosen : " + text_a[4])

    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    itext_b = len(text_b)
    print("deskripsi : ")
    Node = itext_b - 8
    for i in text_b[:Node]:
        print(i)
    print("waktu mulai " + text_b[(itext_b-4)])
    print("waktu mulai " + text_b[(itext_b-2)])

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
    capt = f"""**jenis : {text_a[0]}
jurusan : {text_a[2]}
matkul :  {text_a[3]}
dosen : {text_a[4]}
deskripsi : {desc2}
waktu mulai  {text_b[(itext_b-4)]}
waktu mulai  {text_b[(itext_b-2)]}
**"""
    await bot.send_file(chat, pic_name, caption=capt)
    # download file yang ada pada post

    try:
        file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
        file_name = file.text
        try:
            filez = await bot.upload_file(f'down/{file_name}')
            await bot.send_file(chat, filez)
        except:
            time.sleep(5)
            file.click()
            time.sleep(5)
            filez = await bot.upload_file(f'down/{file_name}')
            await bot.send_file(chat, filez)
    except:
        await bot.send_message(chat, "No File Attached")

    printed_id.append(full_id)
    pickle.dump(printed_id, open("printed_id.p", "wb"))

@bot.on(events.NewMessage(pattern='(?i).*hi'))
async def handler(event):
    await bot.send_message(chat, "test")
    full_id = "dv-progres-sts-194746"
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
    await bot.send_message(chat, f"""jenis : {text_a[0]},
jurusan : {text_a[2]},
matkul :  {text_a[3]},
dosen : {text_a[4]},
deskripsi : {desc2},
waktu mulai  {text_b[(itext_b-4)]},
waktu mulai {text_b[(itext_b-2)]}""")

async def diskusibot(full_id, pic_name):
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")

    ## untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
    itext_b = len(text_b)
    Node = itext_b - 11
    desc =[]
    for i in text_b[6:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)
    ##

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
    try:
        file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
        file_name = file.text
        print(file_name)
    except:
        print("No file attached")

main()
