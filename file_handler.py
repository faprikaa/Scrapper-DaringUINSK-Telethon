import time, os, traceback
from selenium.webdriver.common.by import By
from  bot_handler import *
import traceback
from data_handler import *
from bot_handler import *
import broweb_handler

thisfolder = os.getcwd()
dl_path = thisfolder + r"//down"

browser = broweb_handler.browser

async def files_download(full_id, total_file):
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

async def file_download(full_id):
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
    folder = os.listdir(dl_path)
    if filename.endswith('.'):
        filename = filename[0:-4]
    if filename in folder:
        return filename
    else:
        return Exception
    