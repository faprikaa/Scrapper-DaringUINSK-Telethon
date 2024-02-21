import requests
from bs4 import BeautifulSoup

def cek_komen(post_id):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/load_comments"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    payload = f"id_post={post_id}&type=1&jenistampilan=0"

    cookies = {'PHPSESSID': "qp818hn5eugthgsn9108hb90j5"}
    nama = "Muammar Mufid Darmindra"
    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find("div", string=nama.strip())
    with open("element.html", "w+") as file:
        file.write(parsed.prettify())
    print(search)
    if search:
        if "id" in search.h5.attrs:
            id_komen = search.h5.attrs["id"]
            id_komen_clean = str(id_komen).removeprefix("id-usr-reply-cmt-")
            value_element = search.find_next_sibling("div")
            value_comment = value_element.p.get_text()
        else:
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

def get_komen_id_user(response, nama):
    parsed = BeautifulSoup(response.text, "html.parser")
    search = parsed.find("div", string=nama.strip())
    id_komen = search.h5["id"]
    id_komen2 = str(id_komen).removeprefix("id-usr-reply-cmt-")
    # idkomen = str(id_komen2[1]).removeprefix("wrap_comment")
    return id_komen2


kontol = cek_komen("218461")
# kontol = cek_komen("217297")
print(kontol)