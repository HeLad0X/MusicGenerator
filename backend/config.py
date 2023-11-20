import os
import pathlib

class Config:
    def __init__(self):
        self.__cwd = os.getcwd()
        self.__final_file_path = ''
        self.__data_dir = pathlib.Path('data/maestro-v2.0.0')

    def get_cwd(self):
        return self.__cwd

    def midi_data_path(self):
        return self.__data_dir
    
    def res_file_path(self):
        return self.__final_file_path
    

config = Config()

def get_train_data_path():
    return config.midi_data_path()

def get_current_directory():
    return config.get_cwd()

def download_final_file():
    return config.res_file_path()

