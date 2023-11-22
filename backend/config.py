import os
import pathlib

class Config:
    def __init__(self):
        self.__cwd = os.getcwd()
        self.__final_file_path = ''
        self.__data_dir = pathlib.Path('backend/data/essen/asia')
        self.__dataset_dir = pathlib.Path('backend/cache')
        self.__output_units = None
        self.__model_path = pathlib.Path('backend/models')

    def get_cwd(self):
        return self.__cwd

    def midi_data_path(self):
        return self.__data_dir
    
    def res_file_path(self):
        return self.__final_file_path
    
    def dataset_path(self):
        return self.__dataset_dir
    
    def get_model_path(self, project_id):
        model_folder = os.path.join(self.__model_path,f'{project_id}')
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)

        model_path = os.path.join(model_folder,'model.h5')
        return model_path
    
    def get_single_file_path(self,project_id):
        single_file_name = 'combined_file'
        single_file_folder = os.path.join(self.dataset_path(),f'project{project_id}\\single_file')

        if not os.path.exists(single_file_folder):
            os.makedirs(single_file_folder)

        single_file_path = os.path.join(single_file_folder,single_file_name)

        return single_file_path
    
    def get_multiple_file_path(self,project_id):
        save_data_folder = os.path.join(self.dataset_path(), f'project{project_id}\\multiple_file')

        if not os.path.exists(save_data_folder):
            os.makedirs(save_data_folder)

        return save_data_folder

    def mapping_path(self, project_id):
        mapping_fodler = os.path.join(get_dataset_path(), f'project{project_id}')
        mapping_path = os.path.join(mapping_fodler,'mapping')

        return mapping_path
    
    def set_output_unit(self,num):
        self.__output_units = num
    
    def get_output_unit(self):
        return self.__output_units

LOSS = 'sparse_categorical_crossentropy'
LEARNING_RATE = 0.001
NUM_UNITS = [256]
EPOCHS = 20
BATCH_SIZE = 64
    
ACCEPTABLE_DURATIONS =[
    0.25,
    0.5,
    0.75,
    1.0,
    1.5,
    2,
    3,
    4
]

SEQUENCE_LENGTH = 64

config = Config()

def OUTPUT_UNITS():
    return config.get_output_unit()

def set_output(num):
    config.set_output_unit(num=num)

def get_train_data_path():
    return config.midi_data_path()

def get_current_directory():
    return config.get_cwd()

def download_final_file():
    return config.res_file_path()

def get_dataset_path():
    return config.dataset_path()

def get_single_file_path(project_id):
    return config.get_single_file_path(project_id)

def get_multiple_file_path(project_id):
    return config.get_multiple_file_path(project_id)

def get_mapping_path(project_id):
    return config.mapping_path(project_id)

def get_model_path(project_id):
    return config.get_model_path(project_id=project_id)