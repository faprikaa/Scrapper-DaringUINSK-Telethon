import json

from bs4 import BeautifulSoup

from core.bot import bot
from core.browser import browser
from core.classes.File import FileFromPost
from util.config import CHAT_ID
from utils import ss_element, post_id_to_html_id, generate_caption
from telethon import Button


class Materi:
    def __init__(self, post_id):
        self.id = post_id
        html_id = post_id_to_html_id(post_id)
        self.file = FileFromPost(self.id)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        self.main = soup.find("div", {"id": html_id})
        # self.status = self.main.attrs["class"][2]
        self.parse()
        self.ss_element()

    def download(self):
        if self.file.total_file != 0:
            self.file.files.download()

    def parse(self):
        array_text = self.main.get_text(" | ", strip=True).split(" | ")
        print(array_text)

        self.jenis = array_text[0]
        self.dosen = array_text[1]
        self.jurusan = array_text[2]
        self.matkul = array_text[3]
        self.deskripsi = " ".join(array_text[4: array_text.index('|') - 1])

        # if array_text.index('Waktu Mulai') > array_text.index('|'):
        #     self.deskripsi = " ".join(array_text[5:array_text.index('|') - self.file.total_file])
        # elif array_text.index('Waktu Mulai') < array_text.index('|'):
        #     self.deskripsi = " ".join(array_text[5:array_text.index('Waktu Mulai')])
        # self.waktu_mulai = array_text[array_text.index("Waktu Mulai") + 1].removeprefix(": ")
        # self.waktu_selesai = array_text[array_text.index("Waktu Selesai") + 1].removeprefix(": ")
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
            "waktu_mulai": False,
            "waktu_selesai": False,
            "status":None,
            "waktu_post": self.waktu_post
        }
        return data

    async def send(self):
        capt = generate_caption(self.to_json())
        buttons = [
            Button.inline("Download File", f"download_file_{self.id}"),
            Button.inline("Hapus", "hapus")
        ]
        await bot.send_file(
            entity=CHAT_ID,
            caption=capt,
            file=self.pic_name,
            buttons=buttons
        )
