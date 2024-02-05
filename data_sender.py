import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from data_handler import *
from bot_handler import *
from file_handler import *
from data_parser import *
import broweb_handler

browser = broweb_handler.browser

async def tugasbot(full_id, data=False):
    # pilih id yang mau dipakai
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    parsered = tugas_parser(text_a)
    print(text_a)
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))

    capt = f"""**HTML-ID : ** `{full_id}`
**jenis : **{parsered[0]}
**Jurusan : **{parsered[1]}
**Matkul : **{parsered[2]}
**Dosen : **{parsered[3]}
**Deskripsi : **{parsered[4]}
**Total File : **{total_file}
**Waktu mulai**{parsered[5]}
**Waktu mulai**{parsered[6]}
**Status : **{status}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)
    
    if data:
        #json handler
        data[f"{full_id}"] = {"jenis" : parsered[0], "Jurusan" : parsered[1], "Matkul" : parsered[2], "Dosen" : parsered[3], "Deskripsi" : parsered[4], "Waktu mulai" : parsered[5], "Waktu mulai" : parsered[6], "Status" : status, "Picname" : img_name} 
        return data

async def diskusibot(full_id, data=False):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    status = main.attrs["class"][2]
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    parsered = diskusi_parser(text_a)
    print(text_a)

    ## bot caption maker
    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {parsered[0]}
**Jurusan :** {parsered[1]}
**Matkul :  **{parsered[2]}
**Dosen : **{parsered[3]}
**Indikator Kemampuan : **{parsered[4]}
**Materi Perkuliahan : **{parsered[5]}
**Bentuk Pembelajaran : **{parsered[6]}
**Deskripsi : **{parsered[7]}
**Total File : **{total_file}
**Waktu mulai  **{parsered[8]}
**Waktu selesai  **{parsered[9]}
**Status : **{status}
"""

    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
        data[f"{full_id}"] = {"Jenis" : parsered[0], "Jurusan" : parsered[1], "Matkul" : parsered[2], "Dosen" : parsered[3], "Indikator Kemampuan" : parsered[4], "Materi Perkuliahan" : parsered[5], "Bentuk Pembelajaran" : parsered[6], "Deskripsi" : parsered[7], "Waktu mulai" : parsered[8], "Waktu selesai" : parsered[9], "Status" : status, "Picname" : img_name}
        return data

    # json handler

async def meetingbot(full_id, data=False):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")

    parsered = meeting_parser (text_a)
    link = "https://" + parsered[7]

    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))

    # print text
    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {parsered[0]}
**Jurusan :** {parsered[1]}
**Matkul :  **{parsered[2]}
**Dosen : **{parsered[3]}
**Indikator Kemampuan : **{parsered[4]}
**Materi Perkuliahan : **{parsered[5]}
**Bentuk Pembelajaran : **{parsered[6]}
**Link : ** {link}
**Deskripsi : **{parsered[8]}
**Total File : **{total_file}
**Waktu mulai  **{parsered[9]}
**Waktu selesai  **{parsered[10]}
**Status : **{status}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
        # json handler
        data[f"{full_id}"] = {"Jenis":parsered[0], "Jurusan":parsered[1], "Matkul":parsered[2], "Dosen":parsered[3], "Indikator Kemampuan":parsered[4], "Materi Perkuliahan":parsered[5], "Bentuk Pembelajaran":parsered[6], "Link": link, "Deskripsi":parsered[8], "Total File":total_file, "Waktu mulai  ":parsered[9], "Waktu selesai  " :parsered[10], "Status":status, "Picname" : img_name}
        return data


async def forumbot(full_id, data=False):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip=True).split(" | ")
    dataparser = forum_parser(text_a)

    sub = main.find("div", {"class": "post_content"})
    text_b = sub.get_text(" | ", strip=True).split(" | ")

    total_file = len(browser.find_elements(
        By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    status = "no-status-found"

    # print text
    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {dataparser[0]}
**Jurusan :** {dataparser[1]}
**Matkul :  **{dataparser[2]}
**Nama Pengirim : **{dataparser[3]}
**Deskripsi : **{dataparser[4]}
**Total File : **{total_file}
**Status : **{status}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
    # json handler
        data[f"{full_id}"] = {"Jenis": dataparser[0], "Jurusan": dataparser[1], "Matkul": dataparser[2],"Nama Pengirim": dataparser[3], "Deskripsi": dataparser[4],"Status" : "no-status-found", "Picname": img_name}
        return data

async def materibot(full_id, data=False):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip=True).split(" | ")
    parsered = materi_parser(text_a)

    total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))

    status = "no-status-found"

    # print text
    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {parsered[0]}
**Jurusan :** {parsered[2]}
**Matkul :  **{parsered[3]}
**Nama Pengirim : **{parsered[1]}
**Deskripsi : **{parsered[4]}
**Total File : **{total_file}
**Status : **{status}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)
    if data:
        data[f"{full_id}"] = {"Jenis": parsered[0], "Jurusan": parsered[2], "Matkul": parsered[3],
                          "Nama Pengirim": parsered[1], "Deskripsi": parsered[4],"Status" : "no-status-found", "Picname": img_name}
        return data

    # json handler


async def videobot(full_id, data=False):
        # pilih id yang mau dipakai
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")

    status = main.attrs["class"][2]
    parsered = video_parser(text_a)
    
    total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))
    iframe_vid= browser.find_element(By.XPATH, f'//*[@id="{full_id}"]/div[3]/iframe')
    vid_link = iframe_vid.get_attribute("src")

    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {parsered[0]}
**Jurusan :** {parsered[1]}
**Matkul :  **{parsered[2]}
**Nama Pengirim : **{parsered[3]}
**Deskripsi : **{parsered[4]}
**Video Link : **{vid_link}
**Status : **{status}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
        data[f"{full_id}"] = {"Jenis": parsered[0], "Jurusan": parsered[2], "Matkul": parsered[3], "Nama Pengirim": parsered[1], "Deskripsi": parsered[4], "Video Link": vid_link, "Status": status, "Picname": img_name}
        return data

    # json handler


async def dl_file(total_file, full_id):
    if total_file == 1:
        await file_download( full_id)
    elif total_file == 0:
        await send_msg("No File Attached")
    elif total_file > 1:
        await files_download( full_id, total_file)

def ss_element(full_id):
    img_name = "pic/" + full_id + ".png"
    ele = browser.find_element(By.ID, f"{full_id}")
    browser.execute_script("arguments[0].scrollIntoView(true);", ele)

    if(os.path.exists("pic") != True):
        print("Folders Pict tidak ada, Membuat Folder Pict")
        os.makedirs("pic")
    ele.screenshot(img_name)
    return img_name
