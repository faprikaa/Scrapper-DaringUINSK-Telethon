import json

from core.browser import browser


def get_php_cookie(cookies=None):
    current_cookies = browser.get_cookies()
    if cookies:
        current_cookies = cookies
    for cookie in current_cookies:
        if cookie["name"] == "PHPSESSID":
            return cookie


def insert_cookies_to_browser(browser, cookies):
    for cookie in cookies:
        browser.add_cookie(cookie)


def load_cookies_from_file():
    with open("../cookies.txt", "r+") as file:
        json_cookies = json.load(file)
    return json_cookies


def insert_cookies_to_file(cookies):
    with open("../cookies.txt", "w+") as file:
        json_cookies = json.dumps(cookies, indent=4)
        file.writelines(json_cookies)
