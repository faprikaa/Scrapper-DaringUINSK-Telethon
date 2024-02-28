import re

import requests
from bs4 import BeautifulSoup

from util.cookies import get_php_cookie
from util.web_utils import get_nama_mhs


class Comment:
    def __init__(self, post_id):
        self.total_hadir = None
        self.sudah_komen = False
        self.parsed = None
        self.total_comment = None
        self.id_comment = None
        self.is_nested_comment = None
        self.value_comment = None
        self.value_element = None
        self.post_id = post_id
        self.url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/load_comments"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        self.payload = f"id_post={post_id}&type=1&jenistampilan=0"
        cks = get_php_cookie()
        self.cookies = {'PHPSESSID': cks["value"]}
        self.nama = get_nama_mhs()
        self.cek_komen()
        self.count_hadir()

    def cek_komen(self):
        response = requests.post(self.url, headers=self.headers,
                                 data=self.payload, cookies=self.cookies)
        self.parsed = BeautifulSoup(response.text, "html.parser")
        search = self.parsed.find("div", string=self.nama.strip())
        if search:
            self.sudah_komen = True
            if "id" in search.h5.attrs:  # pakai ini jika komennya di dalam komenan mahasiswa lain
                self.is_nested_comment = True
                id_comment_raw = search.h5.attrs["id"]
                self.id_comment = str(id_comment_raw).removeprefix("id-usr-reply-cmt-")
                self.value_element = search.find_next_sibling("div")
                self.value_comment = self.value_element.p.get_text()
            else:  # pakai ini kalau komen biasa
                self.is_nested_comment = False
                self.value_element = search.find_next_sibling("div")
                id_comment_raw = self.value_element.attrs["id"]
                self.id_comment = str(id_comment_raw).removeprefix("comment")
                self.value_comment = self.value_element.text
        return self.is_nested_comment, self.id_comment, self.value_element, self.value_comment

    def count_hadir(self):
        search = self.parsed.find_all("div", string=re.compile(r'(.*)Hadir(.*)'))
        search2 = self.parsed.find_all("div", string=re.compile(r'(.*)hadir(.*)'))
        self.total_hadir = len(search) + len(search2)
        return self.total_hadir
