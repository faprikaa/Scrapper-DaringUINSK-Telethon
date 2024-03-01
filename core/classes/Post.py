import json

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from telethon import Button

from core.bot import bot
from core.browser import browser
from core.classes.Comment import Comment
from komen.komen import send_komen
from util.config import CHAT_ID, CHECK_COMMENT_EVERY_POST, MINIMAL_COMMENT, DOWNLOAD_PATH
from util.json_util import get_saved_data_by_post_id
from util.web_utils import cek_jenis
from utils import ss_element, post_id_to_html_id, generate_caption


class Post:
    def __init__(self, post_id, from_json=False):
        # fundamental
        self.pic_name = None
        self.id = post_id
        self.html_id = post_id_to_html_id(self.id)
        self.from_json = from_json
        self.jenis = None

        # parse
        self.main = None

        # settings
        self.download_path = DOWNLOAD_PATH

        # file
        self.file_elements = []
        self.total_file = None

        # komen
        self.is_other_commented = None
        self.total_hadir = 0
        self.comment = None
        self.sudah_komen = False

        # data
        self.bentuk_pembelajaran = None
        self.materi_perkuliahan = None
        self.indikator_kemampuan = None
        self.status = None
        self.jenis_iter = None
        self.waktu_post = None
        self.waktu_selesai = None
        self.deskripsi = None
        self.waktu_mulai = None
        self.dosen = None
        self.matkul = None
        self.jurusan = None

        # panggil method
        self.parse()
        self.ss_element()
        self.komen_parse()
        # self.get_file_element()

    def komen_parse(self):
        if self.is_other_commented and CHECK_COMMENT_EVERY_POST:
            self.comment = Comment(self.id)
            self.total_hadir = self.comment.total_hadir
            self.sudah_komen = self.comment.sudah_komen

    async def check_hadir(self):
        if not self.sudah_komen and self.comment.total_hadir > MINIMAL_COMMENT:
            await send_komen(self.id, "Hadir")
            self.sudah_komen = True

    def parse(self):
        if self.from_json:
            datas = get_saved_data_by_post_id(self.id)
            self.file_elements = datas["file_elements"]
            self.pic_name = datas["pic_name"]
            self.jenis = datas["jenis"]
            self.jenis_iter = datas["jenis_iter"]
            self.jurusan = datas["jurusan"]
            self.total_hadir = datas["total_hadir"]
            self.sudah_komen = datas["sudah_komen"]
            self.matkul = datas["mata_kuliah"]
            self.dosen = datas["dosen"]
            self.deskripsi = datas["deskripsi"]
            self.total_file = datas["total_file"]
            self.waktu_mulai = datas["waktu_mulai"]
            self.waktu_selesai = datas["waktu_selesai"]
            self.status = datas["status"]
            self.waktu_post = datas["waktu_post"]
            self.is_other_commented = datas["is_other_commented"]
            return
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        self.main = soup.find("div", {"id": self.html_id})
        file_elements = self.main.find_all("a", {"class": "downloadfile downloadfileset"})
        self.file_elements.extend([str(element) for element in file_elements])
        array_text = self.main.get_text(" | ", strip=True).split(" | ")
        self.jenis = cek_jenis(self.html_id)
        self.total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{self.html_id}"]/div[3]/p'))
        self.is_other_commented = True if len(soup.find("div", {"id": f"commentload{self.id}"})) > 0 else False

        match self.jenis:
            case "Tugas":
                self.jenis_iter = array_text[1]
                self.jurusan = array_text[2]
                self.matkul = array_text[3]
                self.dosen = array_text[4]
                self.status = self.main.attrs["class"][2]
                if array_text.index('Waktu Mulai') > array_text.index('|'):
                    self.deskripsi = " ".join(array_text[5:array_text.index('|') - self.total_file])
                elif array_text.index('Waktu Mulai') < array_text.index('|'):
                    self.deskripsi = " ".join(array_text[5:array_text.index('Waktu Mulai')])
                self.waktu_mulai = array_text[array_text.index("Waktu Mulai") + 1].removeprefix(": ")
                self.waktu_selesai = array_text[array_text.index("Waktu Selesai") + 1].removeprefix(": ")
                self.waktu_post = array_text[-1]
            case "Materi":
                self.dosen = array_text[1]
                self.jurusan = array_text[2]
                self.matkul = array_text[3]
                self.deskripsi = " ".join(array_text[4: array_text.index('|') - 1])
                self.waktu_post = array_text[-1]
            case "Diskusi":
                self.jenis_iter = array_text[2]
                self.jurusan = array_text[3]
                self.matkul = array_text[4]
                self.dosen = array_text[5]
                self.status = self.main.attrs["class"][2]
                self.indikator_kemampuan = array_text[7]
                self.materi_perkuliahan = array_text[9]
                self.bentuk_pembelajaran = array_text[11]
                self.deskripsi = " ".join(array_text[12: array_text.index("Waktu Mulai")])
                self.waktu_mulai = array_text[array_text.index("Waktu Mulai") + 1].removeprefix(": ")
                self.waktu_selesai = array_text[array_text.index("Waktu Selesai") + 1].removeprefix(": ")
                self.waktu_post = array_text[-1]
            case "Pengumuman":
                self.dosen = array_text[1]
                self.jurusan = array_text[2]
                self.matkul = array_text[3]
                self.deskripsi = " ".join(array_text[4: array_text.index("setuju")])
                self.waktu_post = array_text[-1]
            case default:
                ""

    def ss_element(self):
        self.pic_name = ss_element(post_id_to_html_id(self.id))

    def to_json(self):
        data = {
            "post_id": self.id,
            "pic_name": self.pic_name,
            "file_elements": self.file_elements,
            "jenis": self.jenis,
            "jenis_iter": self.jenis_iter,
            "jurusan": self.jurusan,
            "total_hadir": self.total_hadir,
            "sudah_komen": self.sudah_komen,
            "is_other_commented": self.is_other_commented,
            "mata_kuliah": self.matkul,
            "dosen": self.dosen,
            "deskripsi": self.deskripsi,
            "total_file": self.total_file,
            "waktu_mulai": self.waktu_mulai,
            "waktu_selesai": self.waktu_selesai,
            "status": self.status,
            "waktu_post": self.waktu_post
        }
        return data

    def generate_button(self, full=False):
        if full:
            btn_capt = Button.inline("Kembali", f"mini_capt_{self.id}")
        else:
            btn_capt = Button.inline("Selengkapnya", f"full_capt_{self.id}")

        if self.total_file > 0:
            buttons = [
                [
                    btn_capt,
                    Button.inline("Hapus", "hapus")
                ], [
                    Button.inline("Download File", f"download_file_{self.id}"),
                ]
            ]
        else:
            buttons = [
                [
                    btn_capt,
                    Button.inline("Hapus", "hapus")
                ]
            ]
        return buttons

    def save_data(self):
        with open("data.json", "r+") as file:
            data = json.load(file)
            if self.id not in data:
                data[self.id] = self.to_json()
                file.seek(0)  # Move the file pointer to the beginning
                json.dump(data, file, indent=4, sort_keys=True)
                file.truncate()  # Truncate the remaining content (if any)

    async def send(self, full=False):
        capt = generate_caption(self.to_json(), full)
        buttons = self.generate_button()
        await bot.send_file(
            entity=CHAT_ID,
            caption=capt,
            file=self.pic_name,
            buttons=buttons
        )
