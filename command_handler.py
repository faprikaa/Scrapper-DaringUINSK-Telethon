import asyncio, selenium, time
from data_handler import *
from bot_handler import *
from broweb_handler import *
from selenium.common.exceptions import *

def init_bot_cmd(browsers):
    global bot, browser
    browser = browsers
    bot = bot_prepare()

@bot.on(events.NewMessage(pattern='(?i)/*cek'))
async def handler(event):
    await send_msg("Melakukan Cek")
    arr_id = cek_id(browser)
    try:
        msg = await cek_jenis_all(browser, arr_id)
        await send_msg(msg)
    except UnexpectedAlertPresentException : 
        await send_msg("Cookies habis, mengambil ulang")
        await login()
        msg = await cek_jenis_all(browser, arr_id)
        await send_msg(msg)
    except:
        await send_msg(f"An error occured at cek, {traceback.format_exc()}")

@bot.on(events.NewMessage(pattern='(?i)/*fcek'))
async def handler(event):
    await send_msg("Melakukan Force Cek")
    arr_id = cek_id(browser)
    try:
        await force_cek_jenis_all(browser, arr_id)
    except UnexpectedAlertPresentException:
        await send_msg("Cookies habis, mengambil ulang")
        await login()
        msg = await cek_jenis_all(browser, arr_id, data)
        await send_msg(msg)
    except:
        await send_msg(f"An error occured at fcek, {traceback.format_exc()}")

@bot.on(events.NewMessage(pattern='(?i)/ss'))
async def handler(event):
    try:
        pic_name = str(time.time()) + ".png"
        thisfolder = os.getcwd()
        pic_path = thisfolder + r"//pic//"
        picName = pic_path + pic_name
        browser.save_screenshot(picName)
        await send_pic(picName)
    except:
        await send_msg(f"An error occured at fcek, {traceback.format_exc()}")
    
@bot.on(events.NewMessage(pattern='(?i)/*next'))
async def handler(event):
    try:
        button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[12]/center/button")
        click = button.click()
        await send_msg("Tombol Perlihatkan Sebelumnya berhasil di klik !!")
    except UnexpectedAlertPresentException:
        await login()
    except:
        await send_msg(f"An error occured at fcek, {traceback.format_exc()}")

@bot.on(events.NewMessage(pattern='(?i)/*scroll (-?\d+)'))
async def handler(event):
    message = event.pattern_match.group(1)
    try:
        print(message)
        browser.execute_script(f"window.scrollBy(0,{message})")
        await send_msg(f"Berhasil scroll {message} pixel")
    except UnexpectedAlertPresentException:
        await login()
    except:
        await send_msg(f"An error occured at fcek, {traceback.format_exc()}")
    
@bot.on(events.NewMessage(pattern='(?i)/*s2croll (-?\d+)'))
async def handler(event):
    message = event.pattern_match.group(1)
    try:
        browser.execute_script(f"window.scrollBy(0,{message})")
        pic_name = str(time.time()) + ".png"
        thisfolder = os.getcwd()
        pic_path = thisfolder + r"//pic//"
        picName = pic_path + pic_name
        browser.save_screenshot(picName)
        await send_pic(picName)
        await send_msg(f"Berhasil scroll {message} pixel")
    except UnexpectedAlertPresentException:
        await login()
    except:
        await send_msg(f"An error occured at fcek, {traceback.format_exc()}")

@bot.on(events.NewMessage(pattern='(?i)/*help'))
async def handler(event):
    msg = f""" **# Command List **
`/cek` = Menegecek web apa ada postingan baru dengan menggunakan data.json
`/fcek` = Menegecek web apa ada postingan baru TANPA dengan menggunakan data.json
`/ss` = Mengambil screenschot pada browser
`/scroll` [pixel] = Menscroll browser 
`/sscroll` [pixel]= Menscroll browser lalu mengambil screenshot

**# Usage ** 
positif [pixel] untuk ke atas (/scroll 100), negatif [pixel] untuk ke bawah (/scroll -100))
""" 
    await send_msg(msg)