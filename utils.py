import os

from dotmap import DotMap
from selenium.webdriver.common.by import By

from core.browser import browser


def ss_element(html_id):
    img_name = "pic/" + html_id + ".png"
    ele = browser.find_element(By.ID, f"{html_id}")
    browser.execute_script("arguments[0].scrollIntoView(true);", ele)

    if not os.path.exists("pic"):
        print("Folders Pict tidak ada, Membuat Folder Pict")
        os.makedirs("pic")
    ele.screenshot(img_name)
    return img_name


def generate_caption(data, full):
    caption = ""
    data = DotMap(data)
    if not full:
        caption += data.mata_kuliah + "\n"
        caption += f"`{data.post_id}` | " + data.jenis + " | " + (data.jenis_iter if data.jenis_iter else "") + "\n"
        caption += data.dosen + "\n\n"
        caption += "**Deskripsi : **\n" + data.deskripsi + "\n\n"
        if data.total_hadir > 1:
            if data.sudah_komen:
                caption += "**Komen Absen : ** Sudah\n"
            else:
                caption += "**Komen Absen : ** Belum\n"
        else:
            caption += "**Komen Absen : ** Tidak Perlu\n"
        caption += "**Mulai : **" + str(data.waktu_mulai) + "\n"
        caption += "**Selesai : **" + str(data.waktu_selesai) + "\n"
        caption += "**Diposting : **" + data.waktu_post + "\n"
        return caption

    if data.post_id:
        caption += "**Post ID : **\n" + f"`{data.post_id}`" + "\n\n"
    if data.jenis:
        caption += "**Jenis : **\n" + data.jenis + (data.jenis_iter if data.jenis_iter else "") + "\n\n"
    if data.jurusan:
        caption += "**Jurusan : **\n" + data.jurusan + "\n\n"
    if data.mata_kuliah:
        caption += "**Mata Kuliah : **\n" + data.mata_kuliah + "\n\n"
    if data.dosen:
        caption += "**Dosen : **\n" + data.dosen + "\n\n"
    if data.deskripsi:
        caption += "**Deskripsi : **\n" + data.deskripsi + "\n\n"
    if data.total_file:
        caption += "**Total File : **\n" + str(data.total_file) + "\n\n"
    if data.total_hadir:
        caption += "**Total Hadir : **" + str(data.total_hadir) + "\n"
    if data.sudah_absen and data.total_hadir > 1:
        caption += "**Sudah Absen : **" + str(data.sudah_komen) + "\n"
    if data.waktu_mulai:
        caption += "**Waktu Mulai : **\n" + data.waktu_mulai + "\n\n"
    if data.waktu_selesai:
        caption += "**Waktu Selesai : **\n" + str(data.waktu_selesai) + "\n\n"
    caption += "**Waktu Diposting : **\n" + str(data.waktu_post) + "\n\n"
    return caption


def post_id_to_html_id(post_id: str):
    return f"dv-progres-sts-{post_id}"


def html_id_to_post_id(html_id: str):
    return html_id.removeprefix("dv-progres-sts-")
