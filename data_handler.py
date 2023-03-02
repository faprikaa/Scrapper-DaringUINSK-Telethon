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

async def cek_jenis_all(browser, all_id, data):
    data = data
    for full_id in all_id:
        jenis = cek_jenis(browser, full_id)
        try:
            msg = "Ada update tugas "
            if full_id not in data:
                if jenis=="Tugas":
                    data = await tugasbot(browser, full_id, data)
                elif jenis=="Diskusi":
                    data = await diskusibot(browser, full_id, data)
                elif jenis=="Meeting":
                    data = await meetingbot(browser, full_id, data)
                    '''
                elif jenis=="Forum":
                    data = await forumbot(browser, full_id, data)
                    '''
                else:
                    await send_msg(f"Unknown post type, {jenis}")
            elif full_id in data:
                status = status_checker(browser, full_id)
                if data[full_id]["Status"] != status:
                    if jenis=="Tugas":
                        data = await tugasbot(browser, full_id, data)
                    elif jenis=="Diskusi":
                        data = await diskusibot(browser, full_id, data)
                    elif jenis=="Meeting":
                        data = await meetingbot(browser, full_id, data)
                    '''
                    elif jenis=="Forum":
                        data = await forumbot(browser, full_id, data)
                    '''
                    else:
                        await send_msg(f"Unknown post type, {jenis}")
                else:
                    msg = "Tidak ada update tugas"
                    pass
            else:
                msg = "Tidak ada update tugas"
        except Exception as e:
           await send_msg(f"An error occured, {traceback.format_exc()}")

    #json write
    with open(jsonfile, "w") as file:
        json.dump(data, file,  indent=4, sort_keys=True)
    
    return msg

async def force_cek_jenis_all(browser, all_id):
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
            '''
            elif jenis=="Forum":
                data = await forumbot(browser, full_id, data)
            '''
            else:
                await send_msg(f"Unknown post type, {jenis}")
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    pass

