import time, os, traceback
from selenium.webdriver.common.by import By
import bot_handler
import traceback
from data_handler import *
from bot_handler import *
from broweb_handler import *

send_msg = bot_handler.send_msg
send_file = bot_handler.send_file

async def files_download(browser, full_id, total_file):
    try:
        for i in range(1, total_file +1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            file_name = file.text
            path =  os.path.isfile("down/" + file_name)
            if path == False:
                try :
                    clickable.click()
                    time.sleep(5)
                    await send_file(f"{file_name}")
                except:
                    await send_msg(f"An error occured, {traceback.format_exc()}")
                    pass 
            elif path == True:
                try:
                    await send_file(f"{file_name}")
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
        file_name = file.text
        path =  os.path.isfile("down/" + file_name)
        if path == False:
            try :
                clickable.click()
                time.sleep(5)
                await send_file(file_name)
            except:
                await send_msg(f"An error occured, {traceback.format_exc()}")
                pass 
        elif path == True:
            try:
                await send_file(file_name)
            except Exception as e:
                await send_msg(f"An error occured, {traceback.format_exc()}")
                pass
        return True
    except :
        return  traceback.format_exc()  
