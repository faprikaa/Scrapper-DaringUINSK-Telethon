import os

import requests
from bs4 import BeautifulSoup as bs

from util.config import DOWNLOAD_PATH

ele = "<a class=\"downloadfile downloadfileset\" href=\"https://daring.uin-suka.ac.id/attc/199580\" rel=\"https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/get_file_stats/199580\">INTRODUCTION_TO_IRS.pptx</a>"
parsed = bs(ele, "html.parser").find('a')
link = parsed.get("href")
print(parsed)
file_name = parsed.text
cookies = {"PHPSESSID": "v67jivu1a1jplk3aqf0gvpn181"}
res = requests.get(link, cookies=cookies)
with open(file_name, "wb") as file:
    file.write(res.content)
print(res.is_redirect)
print(res.is_permanent_redirect)
print(str(res.text) == "")
