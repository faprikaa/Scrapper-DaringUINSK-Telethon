import os

from selenium.webdriver.common.by import By

from bot_handler import config, send_file
from broweb_handler import browser


class FileFromPost:
    def __init__(self, post_id):
        current_folder = os.getcwd()
        self.post_id = post_id
        self.download_path = os.path.join(current_folder, str(config.get('Driver', 'download_path')))
        self.total_file = len(browser.find_elements(By.XPATH, f'//*[@id="{post_id}"]/div[3]/p'))
        self.name = []
        self.link = []
        self.clickable = []
        self.path = []
        self.is_downloaded = []
        self.file_element = []

        if self.total_file > 1:
            self.get_multi_file_information()
        else:
            self.get_file_information()

    def get_multi_file_information(self):
        for i in range(1, self.total_file + 1):
            file_element = browser.find_element(By.XPATH, f'//*[@id="{self.post_id}"]/div[3]/p[{i}]/span/a')
            self.file_element.append(file_element)
            file = File(file_element)
            self.name.append(file.name)
            self.link.append(file.link)
            self.clickable.append(file.clickable)
            self.path.append(file.path)
            self.is_downloaded.append(file.is_downloaded)

    def get_file_information(self):
        self.file_element = browser.find_element(By.XPATH, f'//*[@id="{self.post_id}"]/div[3]/p/span/a')
        file = File(self.file_element)
        self.name = file.name
        self.link = file.link
        self.clickable = file.clickable
        self.path = file.path
        self.is_downloaded = file.is_downloaded

    def download_file(self):
        if self.total_file > 1:
            for clickable in self.clickable:
                clickable.click()

        else:
            # noinspection PyUnresolvedReferences
            self.clickable.click()

    async def send_file(self, overwrite=True):
        if overwrite or not self.is_downloaded:
            self.download_file()
        if self.total_file > 1:
            for path in self.path:
                await send_file(path)
        else:
            await send_file(self.path)


class File:
    def __init__(self, file_element):
        self.element = file_element
        thisfolder = os.getcwd()
        self.download_path = os.path.join(thisfolder, str(config.get('Driver', 'download_path')))
        self.name = self.get_file_name_from_element()
        self.link = self.element.get_attribute("href")
        self.clickable = self.element.find_element(By.XPATH, f"//a[@href='{self.link}']")
        self.path = os.path.join(self.download_path, self.name)
        self.is_downloaded = os.path.isfile(self.path)

    def download_file(self):
        self.clickable.click()

    async def send_file(self, overwrite=True):
        if overwrite or not self.is_downloaded:
            self.download_file()
            self.is_downloaded = True
        await send_file(self.path)

    def get_file_name_from_folder(self, partial_filename):
        for filename in os.listdir(self.download_path):
            if filename.startswith(partial_filename):
                return filename  # to get  the first found file

    def get_file_name_from_element(self):
        folder = os.listdir(self.download_path)
        element_text = self.element.text
        if element_text.endswith('.'):
            sliced_filename = element_text[0:-4]
            filename = self.get_file_name_from_folder(sliced_filename)
            return filename
        elif element_text in folder:
            return element_text
        else:
            return ""
