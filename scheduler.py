from configparser import ConfigParser
import datetime, time, calendar, sys
import pytz
from data_handler import *

config = ConfigParser()
config.read('config.ini')

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
waktu_jadwal = False
send_notif = False

jam_belajar = []

def hari_parser(hari):
    try:
        hari_arr = hari.split(", ")
        return hari_arr
    except :
        print(Exception)

async def menit_checker(t1, t2):
    global waktu_jadwal, sudah_cek
    if t1 <= jam_ini <= t2:
        ids = cek_id(browser)
        cek = await cek_jenis_all(browser, ids)

        if cek == "tidak ada postingan baru":
            sudah_cek += 1
        else:
            await send_msg(f"Sudah melakukan {sudah_cek} cek dan menemukan postingan baru")
            await send_msg(cek)

        waktu_jadwal = True
        await time_checker()
    elif jam_ini == t2 :
        await send_ms(f"Sudah melakukan {sudah_cek} cek dan saat ini tidak dalam waktu scheduler")
        time.sleep(60)
        waktu_jadwal = False
    else :
        waktu_jadwal = False
        pass

async def checker(arr_jam):
    for jam in arr_jam:
        jams = jam.split(" - ")
        # await cookies_checker()
        await menit_checker(jams[0], jams[1])

async def schedul():
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

async def time_checker():
    global send_notif
    if waktu_jadwal == True and send_notif == False:
        await send_msg("Memasuki waktu jadwal dan auto scrape mode")
        send_notif = True
    elif waktu_jadwal == False:
        send_notif = False
        pass

async def init_schedul(browsers, datas):
    global data, browser
    data = datas
    browser = browsers
    await send_msg("Scheduler Berjalan !!")
