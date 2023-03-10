import psutil, os, scheduler
from data_handler import *
from bot_handler import *
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
    except:
        cmd = event.pattern_match.group(1).strip().lower()
    try:
        if cmd == '':
            arr_id = cek_id()
            await send_msg("Melakukan Cek")
            msg = await cek_jenis_all(arr_id)
            await send_msg(msg)
        elif cmd == 'next':
            await send_msg("Melakukan Cek Next")
            next = click_next()
            arr_id = cek_id()
            arr_id2 = arr_id[-5:]
            msg = await cek_jenis_all(arr_id2)
            await send_msg(msg)
        elif cmd <= 5:
            await send_msg(f"Melakukan {cmd} Cek")
            arr_id = cek_id()
            arr_id2 = arr_id[0:cmd]
            msg = await cek_jenis_all(arr_id2)
            await send_msg(msg)
    except UnexpectedAlertPresentException : 
        await send_msg("Cookies habis, mengambil ulang")
        await login()
        msg = await cek_jenis_all(arr_id)
        await send_msg(msg)
    except:
        await send_msg(f"An error occured at cek, {traceback.format_exc()}")

@bot.on(events.NewMessage(pattern='/fcek(?:\s|$)(.*)'))
async def handler(event):
    arr_id = cek_id()
    try:
        cmd = int(event.pattern_match.group(1))
    except:
        cmd = event.pattern_match.group(1).strip().lower()

    if cmd == '':   
        try: 
            await send_msg("Melakukan Force Cek")
            await force_cek_jenis_all(arr_id)
        except UnexpectedAlertPresentException:
            await send_msg("Cookies habis, silahkan login ulang")
        except:
            await send_msg(f"An error occured at fcek, {traceback.format_exc()}")
    elif cmd == 'next':
        try:
            await send_msg("Melakukan Force Cek Next")
            next = click_next()
            arr_id = cek_id()
            arr_id2 = arr_id[-5:]
            await force_cek_jenis_all(arr_id2)
        except UnexpectedAlertPresentException:
            await send_msg("Cookies habis, silahkan login ulang")
        except:
            await send_msg(f"An error occured at fcek, {traceback.format_exc()}")
    elif cmd <= 5:
        try:
            await send_msg(f"Melakukan {cmd} Force Cek")
            arr_id = cek_id()
            arr_id2 = arr_id[0:cmd]
            await force_cek_jenis_all(arr_id2)
        except UnexpectedAlertPresentException:
            await send_msg("Cookies habis, silahkan login ulang")
        except:
            await send_msg(f"An error occured at fcek, {traceback.format_exc()}")
    else:
        print(cmd)
        print(type(cmd))
        
@bot.on(events.NewMessage(pattern=r"/ss(?:\s+(.+))?"))
async def handler(event):
    message = event.pattern_match.group(1)

    if message :
        try:
            pic_name = str(time.time()) + ".png"
            thisfolder = os.getcwd()
            pic_path = thisfolder + r"//pic//"
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
            pic_path = thisfolder + r"//pic//"
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
    
@bot.on(events.NewMessage(pattern='/sscroll (-?\d+)'))
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

    await send_msg(f"Total RAM yang terpakai sebesar : `{ram}%`\n Total CPU yang terpakai sebesar : `{cpu}%`" )

def click_next():
    button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[12]/center/button")
    try:
        click = button.click()
        return("Tombol Perlihatkan Sebelumnya berhasil di klik kali !!")
    except UnexpectedAlertPresentException:
        return("Cookies habis silahkan login ulang")
    except ElementNotInteractableException:
        return("Please wait 10 seconds before send this command again")
    except:
        return(f"An error occured at next, {traceback.format_exc()}")
