import asyncio
import selenium
import time
import psutil
import os
import scheduler
from data_handler import *
from bot_handler import *
from komen_handler import *
from broweb_handler import *
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By

browser = broweb_handler.browser
bot = bot_handler.bot

looping = scheduler.looping


@bot.on(events.NewMessage(pattern='/cek(?:\s|$)(.*)'))
async def handler(event):
    try:
        cmd = int(event.pattern_match.group(1)) 

        if cmd <= 5:
            await send_msg(f"Melakukan {cmd} Cek")
            arr_id = await cek_id()
            arr_id2 = arr_id[0:cmd]
            msg = await cek_jenis_all(arr_id2)
            await send_msg(msg)
    except:
        cmd = event.pattern_match.group(1).strip().lower()
        try:
            if cmd == '':
                arr_id = await cek_id()
                await send_msg("Melakukan Cek")
                msg = await cek_jenis_all(arr_id)
                await send_msg(msg)
            elif cmd == 'next':
                await send_msg("Melakukan Cek Next")
                next = click_next()
                arr_id = await cek_id()
                arr_id2 = arr_id[-5:]
                msg = await cek_jenis_all(arr_id2)
                await send_msg(msg)
        except UnexpectedAlertPresentException:
            await send_msg("Cookies habis, mengambil ulang")
            await login()
            msg = await cek_jenis_all(arr_id)
            await send_msg(msg)
        except:
            await send_msg(f"An error occured at cek, {traceback.format_exc()}")


@bot.on(events.NewMessage(pattern='/fcek(?:\s|$)(.*)'))
async def handler(event):
    arr_id = await cek_id()
    argument = event.pattern_match.group(1).strip()

    if argument == "" :
        alert_checker()
        await send_msg("Melakukan Force Cek")
        await force_cek_jenis_all(arr_id)
    elif argument == 'next':
        alert_checker()
        click_next()
        await send_msg("Melakukan Force Cek Next")
        arr_id = await cek_id()
        arr_id2 = arr_id[-5:]
        await force_cek_jenis_all(arr_id2)
    elif int(argument) >= 0 :
        alert_checker()
        await send_msg(f"Melakukan {argument} Force Cek ")
        arr_id = await cek_id()
        arr_id2 = arr_id[0:int(argument)]
        await force_cek_jenis_all(arr_id2)
    else:
        print(argument)
        print(type(argument))

@bot.on(events.NewMessage(pattern=r"/ss(?:\s+(.+))?"))
async def handler(event):
    message = event.pattern_match.group(1)

    if message:
        try:
            pic_name = str(time.time()) + ".png"
            thisfolder = os.getcwd()
            pic_path = thisfolder + r"./pic/"
            ele = browser.find_element(By.ID, message)
            browser.execute_script("arguments[0].scrollIntoView(true);", ele)
            picName = pic_path + pic_name
            browser.save_screenshot(picName)
            await send_pic(picName)
        except NoSuchElementException:
            await send_msg("HTML ID tidak ditemukan")
        except:
            await send_msg(f"An error occured as ss, {traceback.format_exc()}")
    else:
        try:
            pic_name = str(time.time()) + ".png"
            thisfolder = os.getcwd()
            pic_path = thisfolder + r"./pic/"
            picName = pic_path + pic_name
            browser.save_screenshot(picName)
            await send_pic(picName)
        except UnexpectedAlertPresentException:
            await send_msg("Cookies habis silahkan login ulang")
        except:
            await send_msg(f"An error occured at ss, {traceback.format_exc()}")


@bot.on(events.NewMessage(pattern='(?i)/*next'))
async def handler(event):
    hasil = click_next()
    await send_msg(hasil)


@bot.on(events.NewMessage(pattern='/scroll (-?\d+)'))
async def handler(event):
    message = event.pattern_match.group(1)
    try:
        browser.execute_script(f"window.scrollBy(0,{message})")
        await send_msg(f"Berhasil scroll {message} pixel")
    except UnexpectedAlertPresentException:
        await login()
    except:
        await send_msg(f"An error occured at scroll, {traceback.format_exc()}")


@bot.on(events.NewMessage(pattern='/s2croll (-?\d+)'))
async def handler(event):
    message = event.pattern_match.group(1)
    try:
        browser.execute_script(f"window.scrollBy(0,{message})")
        pic_name = str(time.time()) + ".png"
        thisfolder = os.getcwd()
        pic_path = thisfolder + r"./pic/"
        picName = pic_path + pic_name
        browser.save_screenshot(picName)
        await send_pic(picName)
        await send_msg(f"Berhasil scroll {message} pixel")
    except UnexpectedAlertPresentException:
        await login()
    except:
        await send_msg(f"An error occured at sscroll, {traceback.format_exc()}")


@bot.on(events.NewMessage(pattern='(?i)/*help'))
async def handler(event):
    msg = f""" **# Command List **
`/cek` = Menegecek web apa ada postingan baru dengan menggunakan data.json
`/fcek` = Menegecek web apa ada postingan baru TANPA dengan menggunakan data.json
`/ss` = Mengambil screenschot pada browser
`/ss [html_id]` = Mengambil screenschot pada browser sesuai id
`/scroll` [pixel] = Menscroll browser 
`/s2croll` [pixel]= Menscroll browser lalu mengambil screenshot
`/loop` = Melihat total loop yang sudah berjalan
`/refresh` = Merefresh halaman daring
`/login` = Melakukan login pada halaman login daring
`/usage` = Melihat RAM dan CPU yang terpakai

**# Usage ** 
positif [pixel] untuk ke atas, ex : /scroll 100
negatif [pixel] untuk ke bawah, ex :/scroll -100
[html-id] adalah id html yang ada pada postingan, ex : /ss dv-progres-sts-20059
"""
    await send_msg(msg)


@bot.on(events.NewMessage(pattern='(?i)/*refresh'))
async def handler(event):
    browser.get("https://daring.uin-suka.ac.id/")
    await send_msg(f"Berhasi melakukan refresh page")


@bot.on(events.NewMessage(pattern='/login(?:\s|$)(.*)'))
async def handler(event):
    cmd = event.pattern_match.group(1).strip().lower()

    if cmd == '':
        await login()
    else:
        await cookies_login(cmd)


@bot.on(events.NewMessage(pattern='(?i)/*usage'))
async def handler(event):
    ram = psutil.virtual_memory()[2]
    cpu = psutil.cpu_percent(4)

    await send_msg(f"Total RAM yang terpakai sebesar : `{ram}%`\n Total CPU yang terpakai sebesar : `{cpu}%`")


@bot.on(events.NewMessage(pattern=r"/cekkomen(?:\s+(.+))?"))
async def handler(event):
    message = event.pattern_match.group(1)

    if message:
        try:
            hasil = cek_komen(message)
            msg = f" {hasil[0]} \nvalue : {hasil[1]}"
            await send_msg(msg)
        except NoSuchElementException:
            await send_msg("HTML ID tidak ditemukan")
        except:
            await send_msg(f"An error occured as ss, {traceback.format_exc()}")
    else:
        await send_msg("harap masukkan id")


@bot.on(events.NewMessage(pattern='/status(?:\s|$)(.*)'))
async def handler(event):
    cmd = event.pattern_match.group(1).strip().lower()
    await send_msg(f"Menjalankan Cek {cmd}")
    if cmd == '':
        await send_msg(f"`ongoing` : untuk postingan yang aktif \n`notyet` : untuk postingan yang belum aktif \n`completed` : untuk postingan yang sudah aktif")
    else:
        cek = await cek_by_status(cmd)
        if cek == "error-01":
            await send_msg("mohon masukan status yang valid")
        elif cek == "error-02":
            await send_msg(f"status {cmd} tidak ditemukan")
