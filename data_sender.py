import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from data_handler import *
from bot_handler import *
from file_handler import *
from data_parser import *

async def tugasbot(browser, full_id, data):
    # pilih id yang mau dipakai
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
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
    # take ss of element
    img_name = "pic/" + full_id +".png"
    ele = browser.find_element(By.ID, f"{full_id}")
    browser.execute_script("arguments[0].scrollIntoView(true);", ele)
    ele.screenshot(img_name)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    if total_file == 1:
        try:
            await file_download(browser, full_id)
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    elif total_file == 0 :
        await send_msg("No File Attached")
    elif total_file > 1:
        try:
            await files_download(browser, full_id, total_file)
        except:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    
    #json handler
    data[f"{full_id}"] = {"jenis" : text_a[0], "Jurusan" : text_a[2], "Matkul" : text_a[3], "Dosen" : text_a[4], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-4)], "Waktu mulai" : text_b[(itext_b-2)], "Status" : status, "Picname" : img_name} 
    return data
    
async def diskusibot(browser, full_id, data):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    status = main.attrs["class"][2]
    text_a = main.get_text(" | ", strip = True ).split(" | ")
    dataparser = diskusiparser(text_a)
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

    # take ss of element
    img_name = "pic/"+full_id +".png"
    ele = browser.find_element(By.ID, f"{full_id}")
    browser.execute_script("arguments[0].scrollIntoView(true);", ele)
    ele.screenshot(img_name)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    if total_file == 1:
        try:
            await file_download(browser, full_id)
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    elif total_file == 0 :
        await send_msg("No File Attached")
    elif total_file > 1:
        try:
            await files_download(browser, full_id, total_file)
        except:
            await send_msg(f"An error occured, {traceback.format_exc()}")

    # json handler
    data[f"{full_id}"] = {"Jenis" : text_a[1], "Jurusan" : text_a[3], "Matkul" : text_a[4], "Dosen" : text_a[5], "Indikator Kemampuan" : text_b[1], "Materi Perkuliahan" : text_b[3], "Bentuk Pembelajaran" : text_b[5], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-7)], "Waktu selesai" : text_b[(itext_b-5)], "Status" : status, "Picname" : img_name}
    return data

async def meetingbot(browser, full_id, data):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
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
    # take ss of element
    img_name = "pic/" +full_id +".png"
    ele = browser.find_element(By.ID, f"{full_id}")
    browser.execute_script("arguments[0].scrollIntoView(true);", ele)
    ele.screenshot(img_name)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    if total_file == 1:
        try:
            await file_download(browser, full_id)
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    elif total_file == 0 :
        await send_msg("No File Attached")
    elif total_file > 1:
        try:
            await files_download(browser, full_id, total_file)
        except:
            await send_msg(f"An error occured, {traceback.format_exc()}")

    # json handler
    data[f"{full_id}"] = {"Jenis" : text_a[1], "Jurusan" : text_a[3], "Matkul" : text_a[4], "Dosen" : text_a[5], "Indikator Kemampuan" : text_b[1], "Materi Perkuliahan" : text_b[3], "Bentuk Pembelajaran" : text_b[5], "lLink" : text_b[6], "Deskripsi" : desc2, "Waktu mulai" : text_b[(itext_b-11)], "Waktu selesai" : text_b[(itext_b-13)], "Status" : status, "Picname" : img_name}
    return data

async def forumbot(browser, full_id, data):
    # ambil text
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find("div", {"id": full_id})
    text_a = main.get_text(" | ", strip=True).split(" | ")
    sub = main.find("div", {"class": "post_content"})
    text_b = sub.get_text(" | ", strip=True).split(" | ")
    total_file = len(browser.find_elements(
        By.XPATH, f'//*[@id="{full_id}"]/div[3]/p'))
    itext_b = len(text_b)

    if total_file > 0:
        total_file2 = total_file * 2 + 2
        Node = itext_b - 13 - total_file2
    else:
        Node = itext_b - 13

     # untuk mengantisipasi jika ada lebih dari 1 line pada deskripsi
    desc = []
    for i in text_b[7:Node]:
        desc.append(i)
    desc2 = "\n".join(desc)

    # print text
    capt = f"""**Jenis :** {text_a[0]}
**Jurusan :** {text_a[2]}
**Matkul :  **{text_a[3]}
**Nama Pengirim : **{text_a[1]}
**Deskripsi : **{desc2}
**Total File : **{total_file}
"""
    # take ss of element
    img_name = "pic/" + full_id + ".png"
    ele = browser.find_element(By.ID, f"{full_id}")
    browser.execute_script("arguments[0].scrollIntoView(true);", ele)
    ele.screenshot(img_name)

    await send_pic(img_name, capt)

    # download file yang ada pada post
    if total_file == 1:
        try:
            await file_download(browser, full_id)
        except Exception as e:
            await send_msg(f"An error occured, {traceback.format_exc()}")
    elif total_file == 0:
        await send_msg("No File Attached")
    elif total_file > 1:
        try:
            await files_download(browser, full_id, total_file)
        except:
            await send_msg(f"An error occured, {traceback.format_exc()}")

    # json handler
    data[f"{full_id}"] = {"Jenis": text_a[0], "Jurusan": text_a[2], "Matkul": text_a[3],
                          "Nama Pengirim": text_a[1], "Deskripsi": desc2, "Picname": img_name}
    return data

