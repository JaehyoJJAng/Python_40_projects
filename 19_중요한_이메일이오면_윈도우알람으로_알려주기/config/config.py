import os
import json
from typing import Optional

def get_secrets(key:str,default_value:Optional[str]=None)-> dict:
    FILE = '.secrets/.secret.json'

    with open(FILE,'r',encoding='UTF-8') as fp:
        secret : dict = json.loads(fp.read())
    try:
        return secret[key]
    except:
        if default_value:
            return default_value
        raise EnvironmentError(f'Set the {key}')