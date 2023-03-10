import json, time
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

config = ConfigParser()
config.read('config.ini')

jsonfile = config.get('Driver', 'json_filename')

browser = broweb_handler.browser

def jsonf_read():
    with open(jsonfile, "r") as file:
        data = json.load(file)
    return data

def cek_jenis(full_id):
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
    except:
        print("using sleep") 
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        time.sleep(5)
        main2 = soup2.find("div", {"id": str(full_id)})
        text_main = main2.get_text(" | ", strip = True ).split(" | ")
    jenis = text_main[0]
    if jenis == "Forum":
        return jenis
    elif jenis == "Tugas":
        return jenis
    elif jenis == "Materi":
        return jenis
    else:
        return (text_main[1])

async def cek_jenis_all(all_id=False, data=False):
    if not data:
        data = jsonf_read()
    if not all_id:
        all_id = cek_id()  

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
        except Exception as e:
           await send_msg(f"An error occured, {traceback.format_exc()}")

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

async def force_cek_jenis_all(all_id):
    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except:
        await send_msg("Cookies habis silahkan login ulang")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
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
            else:
                await send_msg(f"Unknown post type, {jenis}")
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    pass

