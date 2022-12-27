import cryptocode
import glob
import json
import os

class Crypto:
    def __init__(self,password:str)-> None:
        self._password = password

    def encrypt_text(self,text:str)-> str:
        """ 암호화 """
        encoded_string = cryptocode.encrypt(text,password=self._password)
        return encoded_string

    def decrypt_text(self,encoded_text:str)-> str:
        """ 복호화 """
        decoded_string = cryptocode.decrypt(encoded_text,password=self._password)
        return decoded_string

class LoadSecretPassword:
    def __init__(self,jsonFile:str)-> None:
        self.jsonFile = jsonFile

    def load_secret_password(self)-> str:
        with open(self.jsonFile , 'r') as fp:
            secret_password : dict = json.loads(fp.read())
        return secret_password['password']


class GetSecretData:
    def __init__(self,secretFile:str)-> None:
        self._secretFile = secretFile

    def load_secret_data(self)-> str:
        """ secert 파일 데이터 읽어오는 메소드 """
        with open(self._secretFile,'r') as fp:
            text = str(fp.read())
            return text

def main():
    # Get Password
    password = LoadSecretPassword(jsonFile='../.password/.password.json').load_secret_password()

    # Crypto Instance
    crpt = Crypto(password=password)

    # GetSecretData Instance
    secretFile = glob.glob('../secret/*.txt')[0]
    secret = GetSecretData(secretFile=secretFile)

    # 텍스트 데이터 불러오기
    text : str = secret.load_secret_data()

    # 암호화 작업하기
    encoded_string = crpt.encrypt_text(text=text)
    print(encoded_string)

    # 복호화 작업하기
    decoded_string = crpt.decrypt_text(encoded_text=encoded_string)
    print(decoded_string)

if __name__ == '__main__':
    main()