import os
import pathlib

class Files():
    def __init__(self):
        self.folder = str(pathlib.Path(__file__).parent.resolve()) + "\\videos"
    def listVideos(self):
        videos = []
        dir_list = os.listdir(self.folder)
        for file in dir_list:
            if ".mp4" in file:
                videos.append(file)
        return videos
    def folder_files(self):
        return self.folder

