import json

from bs4 import BeautifulSoup

import bot_handler
from bot_handler import send_pic, bot
from broweb_handler import browser
from core.File import FileFromPost
from utils import ss_element, post_id_to_html_id, generate_caption
from telethon import Button


class Tugas:
    def __init__(self, post_id):
        self.id = post_id
        html_id = post_id_to_html_id(post_id)
        self.file = FileFromPost(self.id)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        self.main = soup.find("div", {"id": html_id})
        self.status = self.main.attrs["class"][2]
        self.parse()
        self.ss_element()

    def download(self):
        self.file.download()

    def parse(self):
        array_text = self.main.get_text(" | ", strip=True).split(" | ")
        self.jenis = array_text[0] + " | " + array_text[1]
        self.jurusan = array_text[2]
        self.matkul = array_text[3]
        self.dosen = array_text[4]
        if array_text.index('Waktu Mulai') > array_text.index('|'):
            self.deskripsi = " ".join(array_text[5:array_text.index('|') - self.file.total_file])
        elif array_text.index('Waktu Mulai') < array_text.index('|'):
            self.deskripsi = " ".join(array_text[5:array_text.index('Waktu Mulai')])
        self.waktu_mulai = array_text[array_text.index("Waktu Mulai") + 1].removeprefix(": ")
        self.waktu_selesai = array_text[array_text.index("Waktu Selesai") + 1].removeprefix(": ")
        self.waktu_post = array_text[-1]

    def ss_element(self):
        self.pic_name = ss_element(post_id_to_html_id(self.id))

    def to_json(self):
        data = {
            "post_id": self.id,
            "jenis": self.jenis,
            "jurusan": self.jurusan,
            "mata_kuliah": self.matkul,
            "dosen": self.dosen,
            "deskripsi": self.deskripsi,
            "total_file": self.file.total_file,
            "waktu_mulai": self.waktu_mulai,
            "waktu_selesai": self.waktu_selesai,
            "status": self.status,
            "waktu_post": self.waktu_post
        }
        return data

    async def send(self):
        capt = generate_caption(self.to_json())
        buttons = [
            Button.inline("Download File", f"download_file_{self.id}")
        ]
        await bot.send_file(
            entity=bot_handler.chat,
            caption=capt,
            file=self.pic_name,
            buttons=buttons
        )

