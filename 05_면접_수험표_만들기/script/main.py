""" 
pip install faker : 가짜 데이터 생성하기 위한 라이브러리
pip install python-pptx : 파워포인트 라이브러리
"""
import os
import pandas as pd
from faker import Faker
from pptx import Presentation
from pptx.util import Pt

class GetFaker:
    def __init__(self,fakerPath:str):
        # Faker Instance
        self.faker = Faker('ko_KR')

        # Faker Path
        self.fakerPath = fakerPath

    def get_names(self)-> None:
        """ 가짜이름 생성 메소드 """
        # 가짜 이름 생성
        fake_name_list : list = [self.faker.name() for i in range(10)]

        # 수험번호 생성
        # zfill(3) : 3자리로 빈자리는 0으로 채움
        std_nums : list = [f"2022-{str(i).zfill(3)}" for i in range(1,10 + 1)]

        # Save
        self.save_faker(fake_names=fake_name_list,std_nums=std_nums)

    def save_faker(self,fake_names:list,std_nums:list)-> None:
        fileName = os.path.join(self.fakerPath,'fakers.xlsx')
        if not os.path.exists(self.fakerPath):
            os.mkdir(self.fakerPath)

        df = pd.DataFrame({'이름' : fake_names,'수험번호':std_nums})
        df.to_excel(fileName)

        print(f'{fileName} - 파일 저장 완료!')

class Xlsx:
    def __init__(self,fakerPath:str):
        self.fakerPath = fakerPath

    def load_xlsx(self)-> dict:
        """ 엑셀 파일 읽고 리스트로 저장 """
        df_from_excel = pd.read_excel(os.path.join(self.fakerPath,'fakers.xlsx'))

        data_dic = dict()

        name_list : list = df_from_excel['이름'].to_list()
        std_nums  : list = df_from_excel['수험번호'].to_list()

        data_dic['name_list'] = name_list
        data_dic['std_nums'] = std_nums
        return data_dic

class PPTX:
    def __init__(self,identificationPath:str):
        self.identificationPath = identificationPath

    def load_pptx(self):
        """ PPT 데이터 읽어오는 메소드 """
        # prs = Presentation(os.path.join(self.identificationPath,'수험표_샘플.pptx'))

def make_iter(fakerPath:str,faker_datas:dict):
    """ 반복가능한 객체로 만드는 함수 """
    name_list : list = faker_datas['name_list']
    std_nums  : list = faker_datas['std_nums']

    df_from_excel = pd.read_excel(os.path.join(fakerPath,'fakers.xlsx'))

    # iter() 함수를 사용하여 엑셀에서 읽은 이름 , 수험번호를 반복 가능한 객체로 정의
    name = iter(df_from_excel['이름'])
    std  = iter(df_from_excel['수험번호'])

def main():
    FakerPath = '../faker'
    identificationPath = '../files'

    # Faker 데이터 생성 / 저장
    faker = GetFaker(fakerPath=FakerPath).get_names()

    # Faker 데이터 읽어오기
    faker_datas = Xlsx(fakerPath=FakerPath).load_xlsx()

    # 리스트 안 데이터를 반복 가능한 객체로 만듪기
    make_iter(fakerPath=FakerPath,faker_datas=faker_datas)

    # PPT 데이터 읽어오기
    """PPT 파일이 안열리므로 테스트 불가 (2022.12.25)
     추후 문제 해결되면 commit update"""
    PPTX(identificationPath=identificationPath).load_pptx()

if __name__ == '__main__':
    main()
