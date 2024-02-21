from bs4 import BeautifulSoup
from telethon import Button

from core.bot import bot
from core.browser import browser
from core.classes.File import FileFromPost
from komen.komen import count_hadir, cek_komen
from util.config import CHAT_ID
from util.web_utils import cek_jenis
from utils import ss_element, post_id_to_html_id, generate_caption


class Post:
    def __init__(self, post_id):

        self.bentuk_pembelajaran = None
        self.materi_perkuliahan = None
        self.indikator_kemampuan = None
        self.jenis_iter = None
        self.waktu_post = None
        self.waktu_selesai = None
        self.deskripsi = None
        self.waktu_mulai = None
        self.dosen = None
        self.matkul = None
        self.jurusan = None
        self.jenis = cek_jenis(post_id_to_html_id(post_id))
        self.id = post_id
        html_id = post_id_to_html_id(post_id)
        self.file = FileFromPost(self.id)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        self.main = soup.find("div", {"id": html_id})
        self.is_other_commented = True if len(soup.find("div", {"id": f"commentload{self.id}"})) > 0 else False
        self.status = None
        self.parse()
        self.ss_element()
        if self.is_other_commented:
            self.perlu_absen = True if count_hadir(self.id) > 0 else False
            self.sudah_absen = cek_komen(self.id)["found"] if self.perlu_absen else False
        else:
            self.sudah_absen = None
            self.perlu_absen = None

    def download(self):
        if self.file.total_file != 0:
            self.file.files.download()

    def parse(self):
        array_text = self.main.get_text(" | ", strip=True).split(" | ")
        match self.jenis:
            case "Tugas":
                self.jenis_iter = array_text[1]
                self.jurusan = array_text[2]
                self.matkul = array_text[3]
                self.dosen = array_text[4]
                self.status = self.main.attrs["class"][2]
                if array_text.index('Waktu Mulai') > array_text.index('|'):
                    self.deskripsi = " ".join(array_text[5:array_text.index('|') - self.file.total_file])
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
            "jenis": self.jenis,
            "jenis_iter": self.jenis_iter,
            "jurusan": self.jurusan,
            "perlu_absen" : self.perlu_absen,
            "sudah_absen" : self.sudah_absen,
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

    def generate_button(self, full=False):
        if full:
            btn_capt = Button.inline("Kembali", f"mini_capt_{self.id}")
        else:
            btn_capt = Button.inline("Selengkapnya", f"full_capt_{self.id}")

        if self.file.total_file > 0:
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

    async def send(self, full=False):
        capt = generate_caption(self.to_json(), full)
        buttons = self.generate_button()

        await bot.send_file(
            entity=CHAT_ID,
            caption=capt,
            file=self.pic_name,
            buttons=buttons
        )
