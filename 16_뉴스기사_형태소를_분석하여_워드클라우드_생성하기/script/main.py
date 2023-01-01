from konlpy.tag import Kkma , Komoran , Okt
import requests as rq
import xml.etree.ElementTree as ET
from collections import Counter
import re
from wordcloud import WordCloud
from glob import glob
from typing import List,Dict

class Stemmer:
    def load_stemmer_word(self)-> None:
        """ 형태소 분석 후 출력 """
        kom = Komoran()
        kkm = Kkma()
        okt = Okt()

        text = '일잘러를 위한 파이썬과 40개의 작품들 형태소 분석방법 입니다'
    
        # print(f'kom : {kom.pos(text)}')
        # print(f'kkm : {kkm.pos(text)}')

        print(f'okt : {okt.morphs(text)}')
        print(f'okt 명사 : {okt.nouns(text)}')
    
    def change_word(self,data_list:list)-> List[str]:
        """ 형태소 리스트로 만들어 리턴 """
        okt = Okt()    

        # 명사 담을 리스트 변수 선언
        noun_list : list = list()

        for data in data_list:
            for noun in okt.nouns(data['title']):
                if len(noun) > 1:
                    noun_list.append(noun)

            for noun in okt.nouns(data['description']):
                if len(noun) > 1:
                    noun_list.append(noun)

        # 변환된 형태소 데이터모음 리턴
        return noun_list

    def making_word_cloud(self,noun_list:list)-> None:
        font = glob('../font/*.otf')[0]

        wc = WordCloud(font_path=font,width=400,height=400,scale=2.0,max_font_size=250)

        # 카운터 변환
        counters = Counter(noun_list) 

        gen = wc.generate_from_frequencies(counters)

        # 저장
        wc.to_file('result.png')
class NewsCrawling:
    def __init__(self) -> None:
        # URL
        self.base_url : str = 'https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko'

        # headers
        self.headers : dict = {'User-Agent':'Mozilla/5.0','Content-Type':'text/html; charset=utf-8'}
    
    def get_items(self) -> List[Dict[str,str]]:
        data_list : list = list()        
        with rq.Session() as session:
            with session.get(url=self.base_url,headers=self.headers) as response:
                root_element = ET.fromstring(response.text)
                
                iter_element = root_element.iter(tag='item')
                
                for element in iter_element:
                    data_dic : dict = dict()
                    # 한글 필터링
                    hangul = re.compile('[^ㄱ-ㅣ가-힣]+')

                    # 제목
                    title : str = element.find('title').text

                    # 내용
                    description = hangul.sub('',element.find('description').text)

                    # 데이터 추가
                    data_dic['title'] = title
                    data_dic['description'] = description
                    data_list.append(data_dic)                                    
        return data_list

def main()-> None:
    # Stemmer Instance
    stemmer = Stemmer()

    # NewsCrawling Instance
    crawl = NewsCrawling()

    # 뉴스 데이터 추출
    data_list : list = crawl.get_items()
    
    # 형태소 리스트 추출
    noun_list : list = stemmer.change_word(data_list=data_list)

    # 워드클라우드 저장
    stemmer.making_word_cloud(noun_list=noun_list)
if __name__ == '__main__':
    main()