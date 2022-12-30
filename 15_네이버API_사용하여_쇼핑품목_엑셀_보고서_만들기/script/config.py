import os
import json
from pathlib import Path
from typing import Optional

BASE_DIR : str = '../'

def find_json_file(srcPath:str)-> str:
    for (path,dir,files) in os.walk(srcPath):
        for file in files:
            if '.json' in file:
                secretJson : str = str(os.path.join(path,file))
                return secretJson

def get_api_key(
    key:str,
    default_value : Optional[str] = None
    )-> None:
    secret_json : str = find_json_file(srcPath=BASE_DIR)
    
    with open(secret_json,'r') as fp:
        _secret = json.loads(fp.read())
    
    try:
        return _secret[key]
    except:
        if default_value:
            return default_value
        raise EnvironmentError(f'Set the {key}')