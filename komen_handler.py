import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import broweb_handler
from bot_handler import *

browser = broweb_handler.browser
login = broweb_handler.login
get_cookies = broweb_handler.get_cookies


def cek_komen(full_id):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/load_comments"

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    num_id = full_id.replace("dv-progres-sts-", "")

    payload = f"id_post={num_id}&type=1&jenistampilan=0"

    cks = get_cookies()
    cookies = {'PHPSESSID': cks}
    nama = browser.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b").text
    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find("div", string=nama.strip())
    if search:
        idcmt = get_komen_id(response)
        idkomen2 = "comment" + idcmt
        value = parsed.find(id=idkomen2)
        hasil = ["ditemukan", value.text]
        return hasil
    else:
        return ["tidak-ditemukan", " - "]


async def send_komen(full_id, value):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/comment_stats"

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    num_id = full_id.replace("dv-progres-sts-", "")

    payload = f"jenistampilan=0&content={value}&id_post={num_id}&kd_group=1"

    cks = get_cookies()
    cookies = {'PHPSESSID': cks}
    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    idcmt = get_komen_id(response)
    browser.get("https://daring.uin-suka.ac.id")
    await send_msg(f"Berhasil kirim komentar `{value}` di postingan *{full_id}*")
    cmtclass = "wrap_comment" + idcmt
    try:
        ele = browser.find_element(By.CLASS_NAME, cmtclass)
        img_name = "pic/" + class_bar + ".png"
        browser.execute_script("arguments[0].scrollIntoView(true);", ele)
        ele.screenshot(img_name)
        await send_pic(img_name, "sukses mengirim komentar")
    except:
        pass


def count_hadir(full_id):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/load_comments"

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    num_id = full_id.replace("dv-progres-sts-", "")
    payload = f"id_post={num_id}&type=1&jenistampilan=0"
    cks = get_cookies()
    cookies = {'PHPSESSID': cks}

    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    if response.status_code != 200:
        return response.status_code
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find_all("div", string=re.compile(r'(.*)Hadir(.*)'))
    search2 = parsed.find_all("div", string=re.compile(r'(.*)hadir(.*)'))
    total_search = len(search) + len(search2)
    return total_search


async def auto_hadir(full_id):
    status = broweb_handler.status_checker(full_id)
    if status != "ongoing-progress":
        return None
    cek = cek_komen(full_id)
    total_hadir = count_hadir(full_id)
    if total_hadir > 100:
        await send_msg(f"error {total_hadir} at sending requests")
        return None
    if cek[0] == "tidak-ditemukan":
        if total_hadir >= 4:
            await send_komen(full_id, "hadir")
    else:
        pass


def get_komen_id(response):
    nama = browser.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b").text
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find("div", string=nama.strip())
    div1 = search.previous_element
    div2 = div1.previous_element
    div3 = div2.previous_element
    idkomen = div3.get('class')
    idkomen2 = idkomen[1].replace("wrap_comment", "")
    return idkomen2


@bot.on(events.NewMessage(pattern='/sendkomen(?:\s|$)(.*)'))
async def handler(event):
    fcmd = event.pattern_match.group(1).strip().lower()
    arrcmd = fcmd.split(" ")
    full_id = arrcmd[0]
    arrvalue = arrcmd[1:]
    value = (" ").join(arrvalue)
    if fcmd == '':
        await send_msg("Masukkan HTML-ID dan teks komentar")
    else:
        await send_komen(full_id, value)
