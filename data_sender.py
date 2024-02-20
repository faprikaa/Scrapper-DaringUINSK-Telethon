import pprint
import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from core.File import FileFromPost
from core.post import Tugas
from data_handler import *
from bot_handler import *
from file_handler import *
from data_parser import *
import broweb_handler
from util import ss_element, html_id_to_post_id

browser = broweb_handler.browser

async def tugasbot(full_id, data=False):
    tgs = Tugas(html_id_to_post_id(full_id))
    print(tgs.__dict__)

    # pilih id yang mau dipakai
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    parsered = tugas_parser(text_a)
    files = FileFromPost(full_id)

    waktu = main.find("div", {"class": "time_post"})
    waktu2 = waktu.get('id')

    capt = f"""**HTML-ID : ** `{full_id}`
**jenis : **{parsered[0]}
**Jurusan : **{parsered[1]}
**Matkul : **{parsered[2]}
**Dosen : **{parsered[3]}
**Deskripsi : **{parsered[4]}
**Total File : **{files.total_file}
**Waktu mulai**{parsered[5]}
**Waktu mulai**{parsered[6]}
**Status : **{status}
**Waktu Post : ** {waktu2}
"""
    # take ss of element
    img_name = ss_element(full_id)

    try:
        await send_pic(img_name, capt)
    except MediaCaptionTooLongError:
        print(len(capt))
        capt2 = capt[:512]
        await send_pic(img_name, capt2)

    await files.send_file()
    if data:
        data[f"{full_id}"] = {
            "jenis": parsered[0],
            "Jurusan": parsered[1],
            "Matkul": parsered[2],
            "Dosen": parsered[3],
            "Deskripsi": parsered[4],
            "Waktu mulai": parsered[5],
            "Waktu mulai": parsered[6],
            "Status": status,
            "Picname": img_name,
            "waktu-post": waktu2
        }
        return data

async def diskusibot(full_id, data=False):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    status = main.attrs["class"][2]
    total_file = len(browser.find_elements(By.XPATH,f'//*[@id="{full_id}"]/div[3]/p'))
    parsered = diskusi_parser(text_a)

    waktu = main.find("div", {"class": "time_post"})
    waktu2 = waktu.get('id')

    ## bot2 caption maker
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
**Waktu Post : ** {waktu2}
"""

    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
        data[f"{full_id}"] = {"Jenis" : parsered[0], "Jurusan" : parsered[1], "Matkul" : parsered[2], "Dosen" : parsered[3], "Indikator Kemampuan" : parsered[4], "Materi Perkuliahan" : parsered[5], "Bentuk Pembelajaran" : parsered[6], "Deskripsi" : parsered[7], "Waktu mulai" : parsered[8], "Waktu selesai" : parsered[9], "Status" : status, "Picname" : img_name, "waktu-post" : waktu2}
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

    waktu = main.find("div", {"class": "time_post"})
    waktu2 = waktu.get('id')

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
**Waktu post : ** {waktu2}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
        # json handler
        data[f"{full_id}"] = {"Jenis":parsered[0], "Jurusan":parsered[1], "Matkul":parsered[2], "Dosen":parsered[3], "Indikator Kemampuan":parsered[4], "Materi Perkuliahan":parsered[5], "Bentuk Pembelajaran":parsered[6], "Link": link, "Deskripsi":parsered[8], "Total File":total_file, "Waktu mulai":parsered[9], "Waktu selesai" :parsered[10], "Status":status, "Picname" : img_name, "waktu-post" : waktu2}
        return data

async def forumbot(full_id, data=False):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip=True).split(" | ")
    dataparser = forum_parser(text_a)

    total_file = len(browser.find_elements(
        By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))

    status = "no-status-found"

    waktu = main.find("div", {"class": "time_post"})
    waktu2 = waktu.get('id')

    # print text
    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {dataparser[0]}
**Jurusan :** {dataparser[1]}
**Matkul :  **{dataparser[2]}
**Nama Pengirim : **{dataparser[3]}
**Deskripsi : **{dataparser[4]}
**Total File : **{total_file}
**Status : **{status}
**Waktu post : ** {waktu2}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
    # json handler
        data[f"{full_id}"] = {"Jenis": dataparser[0], "Jurusan": dataparser[1], "Matkul": dataparser[2],"Nama Pengirim": dataparser[3], "Deskripsi": dataparser[4],"Status" : "no-status-found", "Picname": img_name, "waktu-post" : waktu2}
        return data

async def materibot(full_id, data=False):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip=True).split(" | ")
    pprint.pprint(text_a)
    parsered = materi_parser(text_a)

    total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))

    status = "no-status-found"

    waktu = main.find("div", {"class": "time_post"})
    waktu2 = waktu.get('id')

    # print text
    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {parsered[0]}
**Jurusan :** {parsered[2]}
**Matkul :  **{parsered[3]}
**Nama Pengirim : **{parsered[1]}
**Deskripsi : **{parsered[4]}
**Total File : **{total_file}
**Status : **{status}
**Waktu post : ** {waktu2}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)
    if data:
        data[f"{full_id}"] = {"Jenis": parsered[0], "Jurusan": parsered[2], "Matkul": parsered[3],"Nama Pengirim": parsered[1], "Deskripsi": parsered[4],"Status" : "no-status-found", "Picname": img_name, "waktu-post" : waktu2}
        return data

async def videobot(full_id, data=False):
        # pilih id yang mau dipakai
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")

    status = main.attrs["class"][2]
    parsered = video_parser(text_a)

    total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))
    vid_link = get_video_link(full_id)

    waktu = main.find("div", {"class": "time_post"})
    waktu2 = waktu.get('id')
    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {parsered[0]}
**Jurusan :** {parsered[1]}
**Matkul :  **{parsered[2]}
**Nama Pengirim : **{parsered[3]}
**Indikator Kemampuan : **{parsered[4]}
**Materi Perkuliahan : **{parsered[5]}
**Bentuk Pembelajaran : **{parsered[6]}
**Deskripsi : **{parsered[7]}
**Total File : ** {total_file}
**Video Link : **{vid_link}
**Status : **{status}
**Waktu Post : ** {waktu2}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file( total_file, full_id)

    if data:
        data[f"{full_id}"] = {"Jenis": parsered[0], "Jurusan": parsered[1], "Matkul": parsered[2], "Nama Pengirim": parsered[3], "Deskripsi": parsered[4], "Video Link": vid_link, "Status": status, "Picname": img_name, "waktu-post" : waktu2}
        return data

async def pengumumanbot(full_id, data=False):
        # pilih id yang mau dipakai
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    
    parsered = pengumuman_parser(text_a)

    status = "no-status-found"
    total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))

    waktu = main.find("div", {"class": "time_post"})
    waktu2 = waktu.get('id')

    capt = f"""**HTML-ID : ** `{full_id}`
**Jenis :** {parsered[0]}
**Jurusan :** {parsered[1]}
**Matkul :  **{parsered[2]}
**Nama Pengirim : **{parsered[3]}
**Deskripsi : **{parsered[4]}
**Total File** : {total_file}
**Status : **{status}
**Waktu Post : ** {waktu2}
"""
    # take ss of element
    img_name = ss_element(full_id)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    await dl_file(total_file, full_id)
    if data:
        data[f"{full_id}"] = {"Jenis": parsered[0], "Jurusan": parsered[1], "Matkul": parsered[2], "Nama Pengirim": parsered[3], "Deskripsi": parsered[4],"Status": status, "Picname": img_name, "waktu-post" : waktu2}
        return data

async def dl_file(total_file, full_id):
    if total_file == 1:
        await file_download(full_id)
    elif total_file == 0:
        await send_msg("No File Attached")
    elif total_file > 1:
        await files_download(full_id, total_file)




def get_video_link(full_id):
    iframe_vid= browser.find_elements(By.XPATH, f'//*[@id="{full_id}"]/div[3]/iframe')
    total_vid = len(iframe_vid)
    link = []
    for i in range(1, total_vid + 1):
        iframe_vid = browser.find_element(By.XPATH, f'//*[@id="{full_id}"]/div[3]/iframe[{i}]')
        vid_link = iframe_vid.get_attribute("src")
        link.append(vid_link)
    strlink = ", ".join(link)
    return strlink