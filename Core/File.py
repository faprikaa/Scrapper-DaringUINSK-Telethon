import os

from bot_handler import config


class File:

    def __init__(self, post_id):
        self.post_id = post_id
        self.filename = "nofile.txt"
        current_folder = os.getcwd()
        self.download_path = os.path.join(current_folder, str(config.get('Driver', 'download_path')))


    def get_file_name_in_folder(self, partial_filename):
        for filename in os.listdir(self.download_path):
            if filename.startswith(partial_filename):
                self.filename = filename  # to get  the first found file

                

    def download(self):
