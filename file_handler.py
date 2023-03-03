import time, os, traceback
from selenium.webdriver.common.by import By
from  bot_handler import *
import traceback
from data_handler import *
from bot_handler import *
from broweb_handler import *

thisfolder = os.getcwd()
dl_path = thisfolder + r"//down"

async def files_download(browser, full_id, total_file):
    try:
        for i in range(1, total_file +1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            filename = get_file_name(file.text)
            path =  os.path.isfile("down/" + filename)
            if path == False:
                try :
                    clickable.click()
                    time.sleep(5)
                    await send_file(f"{filename}")
                except:
                    await send_msg(f"An error occured, {traceback.format_exc()}")
                    pass 
            elif path == True:
                try:
                    await send_file(f"{filename}")
                except Exception as e:
                    await send_msg(f"An error occured, {traceback.format_exc()}")
                    pass
        return True
    except :
        return  traceback.format_exc()

async def file_download(browser, full_id):
    try :
        file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
        link = file.get_attribute("href")
        clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
        filename = get_file_name(file.text)
        path =  os.path.isfile("down/" + filename)
        if path == False:
            try :
                clickable.click()
                time.sleep(5)
                await send_file(filename)
            except:
                await send_msg(f"An error occured, {traceback.format_exc()}")
                pass 
        elif path == True:
            try:
                await send_file(filename)
            except Exception as e:
                await send_msg(f"An error occured, {traceback.format_exc()}")
                pass
        return True
    except :
        return  traceback.format_exc()  

def get_file_name(filename):
    cut_filename = filename[0:10]
    try:
        folder = os.listdir(dl_path)
        for file in folder:
            if file.startswith(cut_filename):
                final_file_name = file
        return final_file_name
    except Exception as e:
        return e
    
