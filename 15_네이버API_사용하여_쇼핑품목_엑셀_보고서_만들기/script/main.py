from config import get_api_key
import requests as rq
import urllib.parse as rep
import pandas as pd
from io import BytesIO
import PIL
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment
import os

class NaverAPI:
    def __init__(self) -> None:
        self._secrets : dict = get_api_key(key='headers')
    
    def return_secrets(self)-> dict:
        """ 시크릿 키 리턴 """
        return self._secrets    

class SearchKeyword:
    def return_keyword(self)-> str:
        """ 검색어 리턴 """
        while True:
            keyword : str = input('검색어를 입력하세요\n:')
            if not keyword:
                print("검색어가 미입력 되었습니다")
                continue
            return keyword

class CrawlingShopping:
    def __init__(self,secret_keys:dict,keyword:str) -> None:
        self._secret_keys : dict = secret_keys

        self.keyword : str = keyword
        
        self.base_url : str = f'https://openapi.naver.com/v1/search/shop?query={rep.quote_plus(self.keyword)}'

    def fetch(self)-> list:
        options = [f'&display=10&start={1 + (page * 10)}' for page in range(0,2 + 1)]
            
        with rq.Session() as session:
            return [self.get_naver_shopping_items(option=option,session=session) for option in options]            

    def get_naver_shopping_items(self,option:str,session)-> list:
        """ 키워드 상품 리스트 추출 """
        URL : str = self.base_url + option

        with session.get(url=URL,headers=self._secret_keys) as response:
            if response.ok :
                data_list : list = response.json()['items']                
                return data_list

class Pandas:
    def data_save(self,data_list:list):
        """ 추출 데이터 판다스로 저장 """
        # 저장 경로 지정
        savePath : str = '../pandas_data'
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        fileName : str = os.path.join(savePath,'result.xlsx')

        # 판다스 데이터 담을 리스트 변수 선언
        df_list : list = list()

        # 데이터 순회
        for data in data_list:
            df_list.append(pd.DataFrame(data))
        
        d = pd.concat(df_list)
        
        # 파일로 저장
        d.to_excel(fileName)
        print(f'데이터 저장 완료\n{fileName}')

def main()-> None:
    # NaverAPI Instance
    naverAPI = NaverAPI()
    
    # return secert keys
    secret_keys : dict = naverAPI.return_secrets()

    # Keyword Instance
    seo = SearchKeyword()
    
    # keyword 
    keyword : str = seo.return_keyword()

    # CrawlingShopping Instance
    crawl = CrawlingShopping(secret_keys=secret_keys,keyword=keyword)
    
    # Get Items
    data_list : list = crawl.fetch()

    # Pandas Instance
    PD = Pandas()

    # Save using Pandas
    PD.data_save(data_list=data_list)

if __name__ == '__main__':
    main()