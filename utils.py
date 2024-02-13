import os

from selenium.webdriver.common.by import By
from dotmap import DotMap

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


def generate_caption(data):
    caption = ""
    data = DotMap(data)
    if data.post_id:
        caption += "**Post ID : **\n" + data.post_id + "\n\n"
    if data.jenis:
        caption += "**Jenis : **\n" + data.jenis + "\n\n"
    if data.mata_kuliah:
        caption += "**Mata Kuliah : **\n" + data.mata_kuliah + "\n\n"
    if data.dosen:
        caption += "**Dosen : **\n" + data.dosen + "\n\n"
    if data.deskripsi:
        caption += "**Deskripsi : **\n" + data.deskripsi + "\n\n"
    return caption


def post_id_to_html_id(post_id: str):
    return f"dv-progres-sts-{post_id}"


def html_id_to_post_id(html_id: str):
    return html_id.removeprefix("dv-progres-sts-")
