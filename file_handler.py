import time, os, traceback

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from bot_handler import *
import traceback
from data_handler import *
from bot_handler import *
import broweb_handler

thisfolder = os.getcwd()
dl_path = os.path.join(thisfolder, str(config.get('Driver', 'download_path')))

browser = broweb_handler.browser


async def files_download(full_id, total_file):
    try:
        for i in range(1, total_file + 1):
            try:
                file = browser.find_element(By.XPATH, f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            except:
                continue
            await file_download(file_element=file)
        return True
    except:
        raise Exception


async def file_download(full_id=False, file_element=False):
    if not file_element:
        file_element = browser.find_element(By.XPATH, f'//*[@id="{full_id}"]/div[3]/p/span/a')
    file_link = file_element.get_attribute("href")
    file_clickable = browser.find_element(By.XPATH, f"//a[@href='{file_link}']")
    file_name = get_file_name(file_element.text)
    file_path = os.path.join(dl_path, file_name)
    is_file_downloaded = os.path.isfile(file_path)
    try:
        if file_name == "nofile.txt":
            pass
        elif not is_file_downloaded:
            file_clickable.click()
            time.sleep(4)
            await send_file(file_path)
        else:
            await send_file(file_path)
    except Exception as e:
        print(e)


def get_file_name(filename):
    folder = os.listdir(dl_path)
    if filename.endswith('.'):
        sliced_filename = filename[0:-4]
        filename = get_filename_in_folder(sliced_filename)
        return filename
    elif filename in folder:
        return filename
    else:
        return "nofile.txt"


def get_filename_in_folder(partial_filename):
    hasil = "nofile.txt"
    for file_name in os.listdir(dl_path):
        if file_name.startswith(partial_filename):
            hasil = file_name
            return hasil  # to get  the first found file
    return hasil
