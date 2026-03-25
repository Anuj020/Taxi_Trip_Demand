import yaml
from taxidemand.logging.logger import logging
from taxidemand.exception.exception import TaxiDemandException
import os,sys
import dill
import pickle
import numpy as np

# read yaml file
def read_yaml(file_path:str) -> dict:
    try:
        with open(file_path,'rb') as yaml_files:
            return yaml.safe_load(yaml_files)
    except Exception as e:
        raise TaxiDemandException(e,sys)
    
# write yaml file
def write_yaml_file(file_path:str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
            logging.info("content has been dumped.")
    except Exception as e:
        raise TaxiDemandException(e,sys)

# save numpy array in specific file path
def save_numpy_array_data(file_path: str,array: np.array):
    """
    file_path: str location of file to save
    array: array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(dir_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise TaxiDemandException(e,sys)

# load numpy data
def load_numpy_array_data(file_path: str) -> np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file:{file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            np.load(file_path)
            logging.info("numpy array is loaded")
    except Exception as e:
        raise TaxiDemandException(e,sys)
    
# saving objects -- model, preprocesser
def save_object(file_path:str, obj: object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
            logging.info("object has been saved")
    except Exception as e:
        raise TaxiDemandException(e,sys)

# loading objects
def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file:{file_path} is not exists")
        with open(file_path,'rb') as file_obj:
            pickle.load(file_path)
    except Exception as e:
        raise TaxiDemandException(e,sys)

# Evaluate model