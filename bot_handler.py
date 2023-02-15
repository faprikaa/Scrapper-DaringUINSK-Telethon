from lib2to3.pgen2 import driver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pickle, sys, requests, time, asyncio, json, os
from bs4 import BeautifulSoup
from telethon import sync
from telethon import *
from lxml import html
from configparser import ConfigParser
import nest_asyncio
import traceback
nest_asyncio.apply()

def send_var(browser2, soup2, bot2, chat2):
    global browser, soup, bot, chat
    browser = browser2
    soup = soup2
    bot = bot2
    chat = chat2

def json_returner(data_json):
    global data
    data = data_json
    return data

async def tugasbot(full_id, pic_name):
    # pilih id yang mau dipakai
    try :
        main = soup.find("div", {"id": full_id})
        status = main.attrs["class"][2]
    except AttributeError:
        soup2 = BeautifulSoup(soup, 'html.parser')
        main = soup2.find("div", {"id": full_id})
        status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    if total_file > 0 :
        total_file2 = total_file * 2 + 2
        Node = itext_b - 7 - total_file2
    else:
        Node = itext_b - 7

    desc =[]
    for i in text_b[:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)

    if text_b[(itext_b-3)] == "Anda telah mengumpulkan tugas :":
        wkt_mulai = text_b[(itext_b-6)]
        wkt_selesai = text_b[(itext_b-4)]
    else:
        wkt_mulai = text_b[(itext_b-4)]
        wkt_selesai = text_b[(itext_b-2)]

    capt = f"""**jenis : **{text_a[0]}
**Jurusan : **{text_a[2]}
**Matkul : **{text_a[3]}
**Dosen : **{text_a[4]}
**Deskripsi : **{desc2}
**Total File : **{total_file}
**Waktu mulai**{wkt_mulai}
**Waktu mulai**{wkt_selesai}
**Status : **{status}
"""
    await bot.send_file(chat, pic_name, caption=capt)

    #json handler
    data[f"{full_id}"] = {"jenis" : text_a[0], "Jurusan" : text_a[2], "Matkul" : text_a[3], "Dosen" : text_a[4], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-4)], "Waktu mulai" : text_b[(itext_b-2)], "Status" : status, "Picname" : pic_name} 

    # download file yang ada pada post
    if total_file == 1:
        try:
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
            file_name = file.text
            path = os.path.isfile("down/"+file_name)
            if path == False:
                try:                
                    file.click()
                    time.sleep(5)
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except Exception as e:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            elif path == True:
                try:
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except Exception as e:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
        except:
            await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
    elif total_file == 0 :
        await bot.send_message(chat, "No File Attached")
    else :
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
                        file_upload = await bot.upload_file(f'down/{file_name}')
                        await bot.send_file(chat, file_upload)
                    except:
                        await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                        pass 
                elif path == True:
                    try:
                        file_upload = await bot.upload_file(f'down/{file_name}')
                        await bot.send_file(chat, file_upload)
                    except Exception as e:
                        await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                        pass 
        except Exception as  e:
            await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
    
async def diskusibot(full_id, pic_name):
    # ambil text
    try :
        main = soup.find("div", {"id": full_id})
        status = main.attrs["class"][2]
    except AttributeError:
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        main = soup2.find("div", {"id": full_id})
        status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    if total_file > 0 :
        total_file2 = total_file * 2 + 1
        Node = itext_b - 11 - total_file2
    else:
        Node = itext_b - 11
    
    ##untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
    desc =[]
    for i in text_b[6:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)
    
    ## bot caption maker
    capt = f"""**Jenis :** {text_a[1]}
**Jurusan :** {text_a[3]}
**Matkul :  **{text_a[4]}
**Dosen : **{text_a[5]}
**Indikator Kemampuan : **{text_b[1]}
**Materi Perkuliahan : **{text_b[3]}
**Bentuk Pembelajaran : **{text_b[5]}
**Deskripsi : **{desc2}
**Total File : **{total_file}
**Waktu mulai  **{text_b[(itext_b-7)]}
**Waktu selesai  **{text_b[(itext_b-5)]}
**Status : **{status}
"""
    await bot.send_file(chat, pic_name, caption=capt)

    # json handler
    data[f"{full_id}"] = {"Jenis" : text_a[1], "Jurusan" : text_a[3], "Matkul" : text_a[4], "Dosen" : text_a[5], "Indikator Kemampuan" : text_b[1], "Materi Perkuliahan" : text_b[3], "Bentuk Pembelajaran" : text_b[5], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-7)], "Waktu selesai" : text_b[(itext_b-5)], "Status" : status, "Picname" : pic_name}

    # download file yang ada pada post
    if total_file == 1:
        try:
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
            file_name = file.text
            path = os.path.isfile("down/"+file_name)
            if path == False :
                try:
                    file.click()
                    time.sleep(5)
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            elif path == True:
                try:
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except Exception as e:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            else:
                await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                pass 
        except:
            await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
    elif total_file == 0 :
        await bot.send_message(chat, "No File Attached")
    else :
        for i in range(1, total_file + 1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            file_name = file.text
            path = os.path.isfile("down/"+file_name)
            if path == True :
                try:
                    clickable.click()
                    time.sleep(5)
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            elif path == True:
                try:
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except Exception as e:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            else:
                await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                pass 

async def meetingbot(full_id, pic_name):
    # ambil text
    try :
        main = soup.find("div", {"id": full_id})
        status = main.attrs["class"][2]
    except AttributeError:
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        main = soup2.find("div", {"id": full_id})
        status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b= sub.get_text(" | ", strip = True ).split(" | ")
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    if total_file > 0 :
        total_file2 = total_file * 2 + 2
        Node = itext_b - 13 - total_file2
    else:
        Node = itext_b - 13
    
    ##untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
    desc =[]
    for i in text_b[7:Node] : 
        desc.append(i)
    desc2 = "\n".join(desc)
    
    # print text
    capt =f"""**Jenis :** {text_a[1]}
**Jurusan :** {text_a[3]}
**Matkul :  **{text_a[4]}
**Dosen : **{text_a[5]}
**Indikator Kemampuan : **{text_b[1]}
**Materi Perkuliahan : **{text_b[3]}
**Bentuk Pembelajaran : **{text_b[5]}
**Link : **{text_b[6]}
**Deskripsi : **{desc2}
**Total File : **{total_file}
**Waktu mulai  **{text_b[(itext_b-11)]}
**Waktu selesai  **{text_b[(itext_b-13)]}
**Status : **{status}
"""

    #send ke telegram via bot
    await bot.send_file(chat, pic_name, caption=capt)

    # json handler
    data[f"{full_id}"] = {"Jenis" : text_a[1], "Jurusan" : text_a[3], "Matkul" : text_a[4], "Dosen" : text_a[5], "Indikator Kemampuan" : text_b[1], "Materi Perkuliahan" : text_b[3], "Bentuk Pembelajaran" : text_b[5], "lLink" : text_b[6], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-11)], "Waktu selesai" : text_b[(itext_b-13)], "Status" : status, "Picname" : pic_name}

    # download file yang ada pada post
    if total_file == 1:
        try:
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p/span/a')
            file_name = file.text
            file_name = file.text
            path = os.path.isfile("down/"+file_name)
            if path == False :
                try:
                    file.click()
                    time.sleep(5)
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            elif path == True:
                try:
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except Exception as e:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
        except Exception as e:
            await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
    elif total_file == 0 :
        await bot.send_message(chat, "No File Attached")
    else :
        for i in range(1, total_file + 1 ):
            file = browser.find_element(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p[{i}]/span/a')
            link = file.get_attribute("href")
            clickable = browser.find_element(By.XPATH, f"//a[@href='{link}']")
            file_name = file.text
            path = os.path.isfile("down/"+file_name)
            if path == True :
                try:
                    clickable.click()
                    time.sleep(5)
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            elif path == True:
                try:
                    file_upload = await bot.upload_file(f'down/{file_name}')
                    await bot.send_file(chat, file_upload)
                except Exception as e:
                    await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                    pass 
            else:
                await bot.send_message(chat, f"An error occured, {traceback.format_exc()}")
                pass 
