from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from core.browser import browser


def cek_jenis(html_id):
    # print(full_id)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box"))
    )
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    try:
        main = soup.find("div", {"id": str(html_id)})
    except:
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        main = soup.find("div", {"id": str(html_id)})

    try:
        text_main = main.get_text(" | ", strip=True).split(" | ")
    except AttributeError:
        return "err-1"
    except:
        browser.get("https://daring.uin-suka.ac.id/dashboard")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dv-post-box")))
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        main2 = soup2.find("div", {"id": str(html_id)})
        text_main = main2.get_text(" | ", strip=True).split(" | ")

    jenis = text_main[0]
    if jenis == "Forum":
        return jenis
    elif jenis == "Tugas":
        return jenis
    elif jenis == "Materi":
        return jenis
    elif jenis == "Pengumuman":
        return jenis
    else:
        return (text_main[1])


def get_nama_mhs():
    nama = browser.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div/nav/ol/li[1]/div/center/h2/b")
    return nama.text.strip()
