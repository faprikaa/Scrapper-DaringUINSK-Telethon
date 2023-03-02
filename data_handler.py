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

def jsonf_read():
    with open(jsonfile, "r") as file:
        data = json.load(file)
    return data

def cek_jenis(browser, full_id):
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
    else:
        return (text_main[1])

async def cek_jenis_all(browser, all_id, data=0):
    if data==0:
        data = jsonf_read()
    
    browser.get("https://daring.uin-suka.ac.id/dashboard")

    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except:
        await login()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )

    total_tugas_baru = 0 
    for full_id in all_id:
        jenis = cek_jenis(browser, full_id)
        try:
            if full_id not in data:
                if jenis=="Tugas":
                    data = await tugasbot(browser, full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Diskusi":
                    data = await diskusibot(browser, full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis=="Meeting":
                    data = await meetingbot(browser, full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                elif jenis == "Forum":
                    data = await forumbot(browser, full_id, data)
                    total_tugas_baru = total_tugas_baru + 1
                else:
                    await send_msg(f"Unknown post type, {jenis}")
            elif full_id in data:
                status = status_checker(browser, full_id)
                if data[full_id]["Status"] != status:
                    if jenis=="Tugas":
                        data = await tugasbot(browser, full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Diskusi":
                        data = await diskusibot(browser, full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis=="Meeting":
                        data = await meetingbot(browser, full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    elif jenis == "Forum":
                        data = await forumbot(browser, full_id, data)
                        total_tugas_baru = total_tugas_baru + 1
                    else:
                        await send_msg(f"Unknown post type, {jenis}")
        except Exception as e:
           await send_msg(f"An error occured, {traceback.format_exc()}")

    #json write
    with open(jsonfile, "w") as file:
        json.dump(data, file,  indent=4, sort_keys=True)

    # returner
    if total_tugas_baru > 0:
        hasil = f"ada {total_tugas_baru} tugas baru"
        return hasil
    elif total_tugas_baru == 0:
        hasil = "tidak ada postingan baru"
        return hasil

async def force_cek_jenis_all(browser, all_id):
    browser.get("https://daring.uin-suka.ac.id/dashboard")

    try:
        browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    except:
        await login()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    for full_id in all_id:
        jenis = cek_jenis(browser, full_id)
        data= {}
        try:
            if jenis=="Tugas":
                data = await tugasbot(browser, full_id, data)
            elif jenis=="Diskusi":
                data = await diskusibot(browser, full_id, data)
            elif jenis=="Meeting":
                data = await meetingbot(browser, full_id, data)
            elif jenis == "Forum":
                data = await forumbot(browser, full_id, data)
            else:
                await send_msg(f"Unknown post type, {jenis}")
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    pass

