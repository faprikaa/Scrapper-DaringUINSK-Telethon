import os
import time

from bs4 import BeautifulSoup

from core.bot import bot
# from core.browser import browser
from util.config import DOWNLOAD_PATH, CHAT_ID


#
# class FileFromPost:
#     def __init__(self, post_id):
#         self.post_id = post_id
#         self.download_path = os.path.join(os.getcwd(), DOWNLOAD_PATH)
#         self.html_id = post_id_to_html_id(post_id)
#         self.total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{self.html_id}"]/div[3]/p'))
#         if self.total_file == 0:
#             return
#         self.files = []
#
#         if self.total_file > 1:
#             self.get_multi_file_information()
#         else:
#             self.get_file_information()
#
#     def get_multi_file_information(self):
#         for i in range(1, self.total_file + 1):
#             file_element = browser.find_element(By.XPATH, f'//*[@id="{self.html_id}"]/div[3]/p[{i}]/span/a')
#             file = File(file_element, self.download_path)
#             self.files.append(file)
#
#     def get_file_information(self):
#         file_element = browser.find_element(By.XPATH, f'//*[@id="{self.html_id}"]/div[3]/p/span/a')
#         file = File(file_element, self.download_path)
#         self.files.append(file)
#
#     async def send_files(self, overwrite=False, reply_msg_id=None):
#         if reply_msg_id is None:
#             msg = await bot.send_message(CHAT_ID, "Downloading file...")
#         else:
#             msg = await bot.send_message(CHAT_ID, "Downloading file...", reply_to=reply_msg_id)
#
#         try:
#             for file in self.files:
#                 await file.send_file(overwrite=overwrite, progress_msg=msg)
#         finally:
#             await bot.delete_messages(CHAT_ID, [msg])


class File:
    def __init__(self, file_element):
        self.element = file_element
        self.download_path = DOWNLOAD_PATH
        self.parsed = BeautifulSoup(self.element, 'html.parser').find('a')
        self.name = self.get_file_name_from_element()
        self.link = self.parsed.get("href")
        # self.clickable = self.element.find_element(By.XPATH, f"//a[@href='{self.link}']")
        self.path = os.path.join(self.download_path, self.name)
        self.is_downloaded = os.path.isfile(self.path)

    def get_file_name_from_element(self):
        element_text = self.parsed.text
        if element_text.endswith('.'):
            sliced_filename = element_text[:-4]
            for filename in os.listdir(self.download_path):
                if filename.startswith(sliced_filename):
                    return filename
        elif element_text:
            return element_text
        return ""

    def check_is_file_downloaded(self):
        return os.path.isfile(self.path)

    async def send_file(self, overwrite=False, progress_msg=None):
        # if overwrite or not self.is_downloaded:
        # self.clickable.click()

        async def callback(current, total):
            await bot.edit_message(progress_msg, message=f"Uploading {format(current / total, '.2%')}")

        while not self.check_is_file_downloaded():
            time.sleep(1)
        await bot.send_file(CHAT_ID, self.path, progress_callback=callback)
