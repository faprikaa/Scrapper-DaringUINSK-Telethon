from configparser import ConfigParser
import datetime, time, calendar, sys, asyncio
import pytz
from data_handler import *
import broweb_handler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

config = ConfigParser()
config.read('config.ini')

browser = broweb_handler.browser
alert_checker = broweb_handler.alert_checker

stop = 0

Senin = config.get('jadwal', 'Senin')
Selasa = config.get('jadwal', 'Selasa')
Rabu = config.get('jadwal', 'Rabu')
Kamis = config.get('jadwal', 'Kamis')
Jumat = config.get('jadwal', 'Jumat')

time_jakarta =pytz.timezone('Asia/Jakarta')
skrg = datetime.datetime.now(time_jakarta)
hari_ini = skrg.strftime("%A" )
jam_ini = skrg.strftime("%H:%M")

sudah_cek = 0
send_notif = False

jam_belajar = []

def hari_parser(hari):
    try:
        hari_arr = hari.split(", ")
        return hari_arr
    except :
        print(Exception)

async def menit_checker(t1, t2):
    global waktu_jadwal, sudah_cek, send_notif, stop
    while True:
        skrg = datetime.datetime.now(time_jakarta)
        jam_ini = skrg.strftime("%H:%M")
        if stop > 1 :
            await asyncio.sleep(stop)
            stop = 0
            
        if t1 <= jam_ini < t2:
            alert_checker()
            await time_checker(t1 , t2)
            ids = await cek_id()
            browser.get("https://daring.uin-suka.ac.id")
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
            except TimeoutException:
                await send_msg("Cookies habis, login ulang")
                await broweb_handler.login()
            cek = await cek_jenis_all(ids)
            if cek == "tidak ada postingan baru":
                sudah_cek += 1
            else:
                await send_msg(f"Sudah melakukan {sudah_cek} cek dan menemukan postingan baru")
                sudah_cek = 0
            await asyncio.sleep(30)
        elif jam_ini == t2:
            await send_msg(f"Auto scrape berhenti,\nsaat ini **{jam_ini}** dan telah melakukan auto cek sebanyak {sudah_cek}")
            sudah_cek = 0
            send_notif = False
            await asyncio.sleep(60)
            break
        else :
            send_notif = False
            break

async def checker(arr_jam):
    for jam in arr_jam:
        jams = jam.split(" - ")
        # await cookies_checker()
        if jam:
            await menit_checker(jams[0], jams[1])

async def schedul():
    time_jakarta =pytz.timezone('Asia/Jakarta')
    skrg = datetime.datetime.now(time_jakarta)
    hari_ini = skrg.strftime("%A" )
    if hari_ini == "Monday":
        hari = hari_parser(Senin)
        await checker(hari)
    elif hari_ini == "Tuesday":
        hari = hari_parser(Selasa)
        await checker(hari)
    elif hari_ini == "Wednesday":
        hari = hari_parser(Rabu)
        await checker(hari)
    elif hari_ini == "Thursday":
        hari = hari_parser(Kamis)
        await checker(hari)
    elif hari_ini == "Friday":
        hari = hari_parser(Jumat)
        await checker(hari)
    else :
        return None
        pass

async def cookies_checker():
    cooki = browser.get_cookies

    try:
        for i in range(len(cooki)):
            if cooki[i]["name"] == "PHPSESSID":
                expiry_daring = cooki[i]["expiry"]
    except:
        raise Exception
    gmt = time.gmtime()
    timestamp_now = calendar.timegm(gmt)
    try :
        if timestamp_now == expiry_daring:
            await send_msg("Cookies habis ketika akan melakukan scrape, mengambil cookies baru")
            login()
    except:
        pass

async def time_checker(t1,t2):
    skrg = datetime.datetime.now(time_jakarta)
    jam_ini = skrg.strftime("%H:%M")
    hari_ini = skrg.strftime("%A" )
    global send_notif
    if send_notif == False:
        await send_msg(f"Saat ini **{hari_ini}-{jam_ini}** sesuai dengan **{t1}** - **{t2}**\nMemasuki waktu jadwal dan auto scrape mode")
        send_notif = True

async def init_schedul(datas):
    global data
    data = datas
    await send_msg("Scheduler Berjalan !!")

async def looping():
    global total_cek
    total_cek = 1   
    while True:
        try:
            await schedul()
            await reminder()
            await asyncio.sleep(600)
            total_cek += 1
        except :
            await send_msg(f"An error occured at looping, {traceback.format_exc()}")
        
async def scheduler_check():
    time_jakarta =pytz.timezone('Asia/Jakarta')
    skrg = datetime.datetime.now(time_jakarta)
    hari_ini = skrg.strftime("%A" )
    jam_ini2 = skrg.strftime("%H:%M")
    cek = jadwal_check(hari_ini)
    await send_msg(f"waktu saat ini :\nhari : {hari_ini}\njam : {jam_ini2}\njadwal : {cek[1]}\njadwal cek: {cek[0]}")
    
def jadwal_check(hari):
    if hari == "Monday":
        today = Senin
        hari2 = hari_parser(Senin)
    elif hari == "Tuesday":
        today = Selasa
        hari2 = hari_parser(Selasa)
    elif hari == "Wednesday":
        today = Rabu
        hari2 = hari_parser(Rabu)
    elif hari == "Thursday":
        today = Kamis
        hari2 = hari_parser(Kamis)
    elif hari == "Friday":
        today = Jumat
        hari2 = hari_parser(Jumat)
    else :
        return [" - ","tidak ada jadwal"]
    hasil_check = []
    hasil_check.clear()
    for jam in hari2 :
        jams = jam.split(" - ") 
        hasil = jams[0] <= jam_ini < jams[1]
        if hasil :
            hasil_check.append("true")
        else:
            hasil_check.append("false")
    hasil2 = ", ".join(hasil_check)
    hasil_arr = []
    hasil_check.clear()
    hasil_arr.append(hasil2)
    hasil_arr.append(today)
    return hasil_arr

async def reminder():
    time_jakarta =pytz.timezone('Asia/Jakarta')
    skrg = datetime.datetime.now(time_jakarta)
    jam_ini2 = skrg.strftime("%H:%M")
    if jam_ini2 == "07:00":
        cek = await cek_by_status("ongoing")

@bot.on(events.NewMessage(pattern='(?i)/*loop'))
async def handler(event):
    await send_msg(f"Total melakukan loop adalah {total_cek}")
    
@bot.on(events.NewMessage(pattern='(?i)/*schcek'))
async def handler(event):
    await scheduler_check()
    
@bot.on(events.NewMessage(pattern='/stop (-?\d+)'))
async def handler(event):
    message = event.pattern_match.group(1)
    intmsg = int(message)
    try:
        global stop
        await send_msg(f"stop scraping for {intmsg}")
        stop = intmsg
    except UnexpectedAlertPresentException:
        await login()
    except:
        await send_msg(f"An error occured at stop, {traceback.format_exc()}")