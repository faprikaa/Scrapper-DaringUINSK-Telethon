import time, os, traceback
from selenium.webdriver.common.by import By
from  bot_handler import *
import traceback
from data_handler import *
from bot_handler import *
import broweb_handler

thisfolder = os.getcwd()
dl_path = os.path.join(thisfolder, str(config.get('Driver', 'download_path')))

browser = broweb_handler.browser

async def files_download(full_id, total_file):
    try:
        for i in range(1, total_file +1 ):
            try:
                file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            except:
                continue
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            filename = get_file_name(file.text)
            path =  os.path.isfile(dl_path + filename)
            fpath = os.path.join(dl_path, filename)
            if path == False:
                try :
                    clickable.click()
                    while True :
                        time.sleep(1)
                        filename = get_file_name(file.text)
                        if filename != "nofile.txt":
                            fpath = os.path.join(dl_path, filename)
                            await send_file(fpath)
                            break
                except NoSuchElementException:
                    pass 
            elif path == True:
                try:
                    await send_file(fpath)
                except Exception as e:
                    pass
        return True
    except :
        raise Exception

async def file_download(full_id):
    try :
        file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
        link = file.get_attribute("href")
        print(link)
        clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
        filename = get_file_name(file.text)
        path =  os.path.isfile(dl_path + filename)
        fpath = os.path.join(dl_path, filename)
        if path == False or filename == "nofile.txt":
            try :
                clickable.click()
                time.sleep(4)
                filename = get_file_name(file.text)
                if filename != "nofile.txt":
                    await send_file(fpath)
            except NoSuchElementException:
                pass 
        elif path == True:
            try:
                await send_file(fpath)
            except Exception as e:
                pass
        return True
    except Exception as e :
        print(e)

def get_file_name(filename):
    folder = os.listdir(dl_path)
    if filename.endswith('.'):
        pfilename = filename[0:-4]
        filename = get_filename_in_folder(pfilename)
        return filename
    elif filename in folder:
        return filename
    else :
        return "nofile.txt"
    
def get_filename_in_folder(partial_filename):
    for f_name in os.listdir(dl_path):
        if f_name.startswith(partial_filename):
            hasil = f_name
            return hasil
        else:
            hasil = "nofile.txt"
    return hasil