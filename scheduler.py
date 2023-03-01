from configparser import ConfigParser
import datetime, time, calendar, sys
from data_handler import *

config = ConfigParser()
config.read('config.ini')

Senin = config.get('jadwal', 'Senin')
Selasa = config.get('jadwal', 'Selasa')
Rabu = config.get('jadwal', 'Rabu')
Kamis = config.get('jadwal', 'Kamis')
Jumat = config.get('jadwal', 'Jumat')

skrg = datetime.datetime.now()
hari_ini = skrg.strftime("%A" )
jam_ini = skrg.strftime("%H:%M")

i = 0

jam_belajar = []

def hari_parser(hari):
    try:
        hari_arr = hari.split(", ")
        return hari_arr
    except AttributeError: 
        return hari
    except :
        print(Exception)

def menit_checker(t1, t2, browser, data):
    if t1 <= jam_ini <= t2:
        ids = cek_id(browser)
        cek_jenis_all(browser, ids, data)
        i = 0
    else :
        i + 1
        pass

def checker(hari):
    if hari != "":
        arr_jam = hari_parser(hari)
        if type(arr_jam) == str:
            cookies_checker(brw, browser)
            menit_checker(arr_jam[0], arr_jam[1])
        elif type(arr_jam) == list: 
            for jam in arr_jam:
                jams = jam.split(" - ")
                cookies_checker(brw, browser)
                menit_checker(jams[0], jams[1])

def schedul(brws, browsers, datas):
    global brw, browser, data
    browser = browsers
    data = datas
    brw = brws

    if hari_ini == "Monday":
        checker(Senin)
    elif hari_ini == "Tuesday":
        checker(Selasa)
    elif hari_ini == "Wednesday":
        checker(Rabu)
    elif hari_ini == "Thursday":
        checker(Kamis)
    elif hari_ini == "Friday":
        checker(Jumat)

def cookies_checker(brw, browser):
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
            browser = login(brw)
    except:
        pass
