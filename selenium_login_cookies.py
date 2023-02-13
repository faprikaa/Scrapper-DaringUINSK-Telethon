from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pickle, sys, requests, time, asyncio, json, os
from bs4 import BeautifulSoup
from telethon import sync
from telethon import *
from lxml import html
from configparser import ConfigParser
import nest_asyncio

# Read config.ini
config = ConfigParser()
config.read('config.ini')

api_id = config.getint('Telegram_bot', 'api_id')
api_hash = config.get('Telegram_bot', 'api_hash')
bot_token = config.get('Telegram_bot', 'bot_token')
chat = config.getint('Telegram_bot', 'chat')
username = config.get('Login', 'username')
password = config.get('Login', 'password')
jsonfile = "data.json"

bot = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

total_id = []
all_id = []
printed_id = []

options = webdriver.ChromeOptions()
prefs={"download.default_directory":f"{os.getcwd()}\down"};
options.add_experimental_option("prefs",prefs);
ser = Service("driver/chromedriver.exe")
browser = webdriver.Chrome(service=ser ,options=options)
nest_asyncio.apply()

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

async def cek_jenis_all():
    for full_id in all_id:
        total_id.append(full_id)
        pickle.dump(total_id, open("all_id.p", "wb"))
        jenis = cek_jenis(full_id)
        num_id = full_id.replace("dv-progres-sts-","")
        div = browser.find_element(By.XPATH, f'//*[@id="{full_id}"]')
        try:
            post = data[f"{full_id}"] 
            if post is None:
                if jenis=="Tugas":
                    pic_name = take_ss(browser, full_id)
                    loop.run_until_complete(tugasbot(full_id, pic_name))
                elif jenis=="Diskusi":
                    pic_name = take_ss(browser, full_id)
                    loop.run_until_complete(diskusibot(full_id, pic_name))
                elif jenis=="Meeting":
                    pic_name = take_ss(browser, full_id)
                    loop.run_until_complete(meetingbot(full_id, pic_name))
                else:
                    print(jenis)
                    #auto_hadir(num_id)
            else:
                msg = "Tidak ada update tugas"
        except KeyError:
            if jenis=="Tugas":
                pic_name = take_ss(browser, full_id)
                loop.run_until_complete(tugasbot(full_id, pic_name))
            elif jenis=="Diskusi":
                pic_name = take_ss(browser, full_id)
                loop.run_until_complete(diskusibot(full_id, pic_name))
            elif jenis=="Meeting":
                pic_name = take_ss(browser, full_id)
                loop.run_until_complete(meetingbot(full_id, pic_name))
            else:
                msg = "Tidak ada update tugas"
                print(jenis)
                #auto_hadir(num_id)
        except Exception as e:
            raise(e)
    try:
        await bot.send_message(chat, msg)
    except:
        pass

def cek_jenis(full_id):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    bs_id = full_id.replace("dv-progres-sts-","dv-jurnalperkuliahan-")
    main = soup.find("div", {"id": str(full_id)})
    try:
        text_main = main.get_text(" | ", strip = True ).split(" | ")
    except:
        print("using sleep") 
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        time.sleep(10)
        main2 = soup2.find("div", {"id": str(full_id)})
        text_main = main2.get_text(" | ", strip = True ).split(" | ")
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
    global data
    with open(jsonfile, "r") as file:
        data = json.load(file)

async def tugasbot(full_id, pic_name):
    # pilih id yang mau dipakai
    main = soup.find("div", {"id": full_id})
    status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    if total_file > 0 :
        total_file2 = total_file * 2 + 2
        Node = itext_b - 5 - total_file2
    else:
        Node = itext_b - 5

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
**Status : **{status}
"""
    await bot.send_file(chat, pic_name, caption=capt)

    #json handler
    data[f"{full_id}"] = {"jenis" : text_a[0], "Jurusan" : text_a[2], "Matkul" : text_a[3], "Dosen" : text_a[4], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-4)], "Waktu mulai" : text_b[(itext_b-2)], "Status" : status}
    with open(jsonfile, "a") as file:
        json.dump(data, file,  indent=4, sort_keys=True)

    # download file yang ada pada post
    if total_file == 1:
        try:
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
            try:
                file.click()
                time.sleep(2)
                file_upload = await bot.upload_file(f'down/{file_name}')
                await bot.send_file(chat, file_upload)
            except Exception as e:
                print(e)
                pass  
        except:
            raise Exception
    elif total_file == 0 :
        await bot.send_message(chat, "No File Attached")
    else :
        for i in range(1, total_file +1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            file_name = file.text
            try :
                clickable.click()
                time.sleep(2)
                file_upload = await bot.upload_file(f'down/{file_name}')
                await bot.send_file(chat, file_upload)
            except Exception as e:
                print(e)
                pass 
    
async def diskusibot(full_id, pic_name):
    # ambil text
    main = soup.find("div", {"id": full_id})
    status = main.attrs["class"][2]
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
    
    ##untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
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
**Status : **{status}
"""
    await bot.send_file(chat, pic_name, caption=capt)

    # json handler
    data[f"{full_id}"] = {"Jenis" : text_a[1], "Jurusan" : text_a[3], "Matkul" : text_a[4], "Dosen" : text_a[5], "Indikator Kemampuan" : text_b[1], "Materi Perkuliahan" : text_b[3], "Bentuk Pembelajaran" : text_b[5], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-7)], "Waktu selesai" : text_b[(itext_b-5)], "Status" : status}
    with open(jsonfile, "w") as file:
        json.dump(data, file,  indent=4, sort_keys=True)

    # download file yang ada pada post
    if total_file == 1:
        try:
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
            file_name = file.text
            try:
                file.click()
                time.sleep(2)
                file_upload = await bot.upload_file(f'down/{file_name}')
                await bot.send_file(chat, file_upload)
            except Exception as e:
                await bot.send_message(chat, f"Gagal mengirim file karena {e}")
        except:
            raise Exception
    elif total_file == 0 :
        await bot.send_message(chat, "No File Attached")
    else :
        for i in range(1, total_file + 1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            file_name = file.text
            try:
                clickable.click()
                time.sleep(2)
                file_upload = await bot.upload_file(f'down/{file_name}')
                await bot.send_file(chat, file_upload)
            except Exception as e:
                await bot.send_message(chat, f"Gagal mengirim file karena {e}")

async def meetingbot(full_id, pic_name):
    # ambil text
    main = soup.find("div", {"id": full_id})
    status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    if total_file > 0 :
        total_file2 = total_file * 2 + 2
        Node = itext_b - 13 - total_file2
    else:
        Node = itext_b - 13
    
    ##untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
    desc =[]
    for i in text_b[7:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)
    
    # print text
    capt =f"""**Jenis :** {text_a[1]}
**Jurusan :** {text_a[3]}
**Matkul :  **{text_a[4]}
**Dosen : **{text_a[5]}
**Indikator Kemampuan : **{text_b[1]}
**Materi Perkuliahan : **{text_b[3]}
**Bentuk Pembelajaran : **{text_b[5]}
**Link : **{text_b[6]}
**Deskripsi : **{desc2}
**Waktu mulai  **{text_b[(itext_b-11)]}
**Waktu selesai  **{text_b[(itext_b-13)]}
**Status : **{status}
"""

    #send ke telegram via bot
    await bot.send_file(chat, pic_name, caption=capt)

    # json handler
    data[f"{full_id}"] = {"Jenis" : text_a[1], "Jurusan" : text_a[3], "Matkul" : text_a[4], "Dosen" : text_a[5], "Indikator Kemampuan" : text_b[1], "Materi Perkuliahan" : text_b[3], "Bentuk Pembelajaran" : text_b[5], "Link" : text_b[6], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-11)], "Waktu selesai" : text_b[(itext_b-13)], "Status" : status}
    with open(jsonfile, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)

    # download file yang ada pada post
    if total_file == 1:
        try:
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
            file_name = file.text
            try:
                file.click()
                time.sleep(2)
                file_upload = await bot.upload_file(f'down/{file_name}')
                await bot.send_file(chat, file_upload)
            except Exception as e:
                await bot.send_message(chat, f"Gagal mengirim file karena {e}")
        except:
            raise Exception
    elif total_file == 0 :
        await bot.send_message(chat, "No File Attached")
    else :
        for i in range(1, total_file + 1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            file_name = file.text
            try:
                clickable.click()
                time.sleep(2)
                file_upload = await bot.upload_file(f'down/{file_name}')
                await bot.send_file(chat, file_upload)
            except Exception as e:
                await bot.send_message(chat, f"Gagal mengirim file karena {e}")

@bot.on(events.NewMessage(pattern='(?i)/*cek'))
async def handler(event):
    loop.run_until_complete(cek_jenis_all())

def main():
    global loop
    loop = asyncio.get_event_loop() # untuk menjalankan async
    loop.run_until_complete(sel_login()) #login
    scrape(browser.page_source) #persiapan beautiful soup
    cek_id() #mengambil data yang ada pada page
    loop.run_until_complete(cek_jenis_all()) #menganalisis tiap data
    bot.run_until_disconnected()

main()
