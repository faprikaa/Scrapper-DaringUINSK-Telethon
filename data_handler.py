import json, time, asyncio
from configparser import ConfigParser
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import traceback
from data_handler import *
from bot_handler import *
from broweb_handler import *
from data_sender import *
from komen_handler import *

config = ConfigParser()
config.read('config.ini')

jsonfile = config.get('Driver', 'json_filename')

browser = broweb_handler.browser

def jsonf_read():
    with open(jsonfile, "r") as file:
        data = json.load(file)
    return data

def cek_jenis(full_id):
    # print(full_id)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    try:
        main = soup.find("div", {"id": str(full_id)})
    except:
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        main = soup.find("div", {"id": str(full_id)})

    try:
        text_main = main.get_text(" | ", strip = True ).split(" | ")
    except AttributeError:
        return "err-1"
        browser.get("https://google.com")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "k1zIA")))
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        main2 = soup2.find("div", {"id": str(full_id)})
        text_main = main2.get_text(" | ", strip = True ).split(" | ")
    except :
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        main2 = soup2.find("div", {"id": str(full_id)})
        text_main = main2.get_text(" | ", strip = True ).split(" | ")
        print(Exception)
        
    jenis = text_main[0]
    if jenis == "Forum":
        return jenis
    elif jenis == "Tugas":
        return jenis
    elif jenis == "Materi":
        return jenis
    elif jenis== "Pengumuman":
        return jenis
    else:
        return (text_main[1])

async def cek_jenis_all(all_id=False, data=False):
    if not data:
        data = jsonf_read()
    if not all_id:
        all_id = await cek_id()  

    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except:
        await login()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    total_tugas_baru = 0
    for full_id in all_id:
        jenis = cek_jenis(full_id)
        if jenis == "err-1":
            continue
            pass
        try:
            if full_id not in data:
                if jenis=="Tugas":
                    data = await tugasbot(full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Diskusi":
                    data = await diskusibot(full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Meeting":
                    data = await meetingbot(full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Forum":
                    data = await forumbot(full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Materi":
                    data = await materibot(full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Video":
                    data = await videobot(full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Pengumuman":
                    data = await pengumumanbot(full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                else:   
                    await send_msg(f"Unknown post type, {jenis}")
            elif full_id in data:
                status = status_checker(full_id)
                if data[full_id]["Status"] != status:
                    if jenis=="Tugas":
                        data = await tugasbot(full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Diskusi":
                        data = await diskusibot(full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Meeting":
                        data = await meetingbot(full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Forum":
                        data = await forumbot(full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Materi":
                        data = await materibot(full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Video":
                        data = await videobot(full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Pengumuman":
                        data = await pengumumanbot(full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
            await auto_hadir(full_id)
        except Exception as e:
           await send_msg(f"An error occured at cek jnis, {traceback.format_exc()}")

    #json write
    with open(jsonfile, "w") as file:
        json.dump(data, file,  indent=4, sort_keys=True)

    # returner
    if total_tugas_baru > 0:
        hasil = f"ada {total_tugas_baru} postingan baru"
        return hasil
    elif total_tugas_baru == 0:
        hasil = "tidak ada postingan baru"
        return hasil

async def cek_by_status(pm_status):
    total_next = 0
    if pm_status == "ongoing":
        status = "ongoing-progress"
    elif pm_status == "notyet":
        status = "notyet-progress"
    elif pm_status == "completed":
        status = "completed-progress"
    else :
        return "error-01"
    
    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except:
        await login()
        
    arr_post_status = []
    while True:
        all_id = await cek_id()
        for full_id in all_id:
            post_status = status_checker(full_id)
            if post_status == status:
                if full_id not in arr_post_status:
                    arr_post_status.append(full_id)
            else:
                pass
        print(arr_post_status)
        total_post2 = len(arr_post_status)
        if total_post2 < 1 :
            return "error-02"
            break
        elif total_post2 >= 5:
            break
        elif total_post2 < 5:
            if total_next <= 3:
                nxt = click_next()
                total_next += 1
                await asyncio.sleep(5)
                if nxt == "Tombol Perlihatkan Sebelumnya berhasil di klik kali !!":
                    continue
                else:
                    await asyncio.sleep(10)
                    click_next()
                    total_next += 1
            else:
                break
    await force_cek_jenis_all(arr_post_status)
    
async def force_cek_jenis_all(all_id):
    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except:
        await send_msg("Cookies habis silahkan login ulang")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    print(all_id)

    for full_id in all_id:
        jenis = cek_jenis(full_id)
        try:
            if jenis=="Tugas":
                data = await tugasbot(full_id)
            elif jenis=="Diskusi":
                data = await diskusibot(full_id)
            elif jenis=="Meeting":
                data = await meetingbot(full_id)
            elif jenis=="Forum":
                data = await forumbot(full_id)
            elif jenis=="Materi":
                data = await materibot(full_id)
            elif jenis=="Video":
                data = await videobot(full_id)
            elif jenis=="Pengumuman":
                data = await pengumumanbot(full_id)
            else:
                await send_msg(f"Unknown post type, {jenis}")
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
        await auto_hadir(full_id)
    pass

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