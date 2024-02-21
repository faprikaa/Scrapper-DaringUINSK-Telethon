import re

import requests
from bs4 import BeautifulSoup

from util.config import CHAT_ID
from util.cookies import get_php_cookie
from util.web_utils import get_nama_mhs
from core.bot import bot


def cek_komen(post_id):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/load_comments"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    payload = f"id_post={post_id}&type=1&jenistampilan=0"

    cks = get_php_cookie()
    cookies = {'PHPSESSID': cks["value"]}
    nama = get_nama_mhs()
    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find("div", string=nama.strip())
    if search:
        if "id" in search.h5.attrs: # pakai ini jika komennya di dalam komenan mahasiswa lain
            id_komen = search.h5.attrs["id"]
            id_komen_clean = str(id_komen).removeprefix("id-usr-reply-cmt-")
            value_element = search.find_next_sibling("div")
            value_comment = value_element.p.get_text()
        else: #pakai ini kalau komen biasa
            value_element = search.find_next_sibling("div")
            id_komen = value_element.attrs["id"]
            id_komen_clean = str(id_komen).removeprefix("comment")
            value_comment = value_element.text
        return {
            "found": True,
            "text": value_comment,
            "id": id_komen_clean
        }
    else:
        return {
            "found": False,
            "text": None,
            "id": None
        }


def count_hadir(full_id):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/load_comments"

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    num_id = full_id.replace("dv-progres-sts-", "")
    payload = f"id_post={num_id}&type=1&jenistampilan=0"
    cks = get_php_cookie()
    cookies = {'PHPSESSID': cks["value"]}

    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    if response.status_code != 200:
        return response.status_code
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find_all("div", string=re.compile(r'(.*)Hadir(.*)'))
    search2 = parsed.find_all("div", string=re.compile(r'(.*)hadir(.*)'))
    total_search = len(search) + len(search2)
    return total_search


async def send_komen(post_id, value):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/comment_stats"

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    payload = f"jenistampilan=0&content={value}&id_post={post_id}&kd_group=1"

    cks = get_php_cookie()
    cookies = {'PHPSESSID': cks}
    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    if response.status_code == 200:
        await bot.send_message(CHAT_ID, f"Berhasil kirim komentar `{value}` di postingan *{post_id}*")
    else:
        await bot.send_message(CHAT_ID, "Gagal kirim komentar !")


def get_komen_id_user(response, nama):
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find("div", string=nama.strip())
    id_komen = search.h5["id"]
    id_komen2 = str(id_komen).removeprefix("id-usr-reply-cmt-")
    # idkomen = str(id_komen2[1]).removeprefix("wrap_comment")
    return id_komen2
