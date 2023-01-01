from typing import Optional
import json
import os

BASE_DIR = '.token/'
FILE = '.token.json'
def get_telegram_secret(key:str,default_value:Optional[str]=None):
    with open(os.path.join(BASE_DIR,FILE),'r',encoding='UTF-8') as fp:
        data_dic : dict = json.loads(fp.read())
    try:
        return data_dic[key]
    except:
        if default_value:
            return default_value
        raise EnvironmentError(f'Set the {key}') 