from config.config import get_secrets
import pandas as pd
import random
from faker import Faker
from typing import Union
import os
import smtplib
from email.mime.text import MIMEText

class FakerData:
    def create_faker_data(self)-> dict:
        """ 가짜 데이터 생성 """
        faker = Faker('ko_KR')

        faker_dict : dict = dict()

        fake_name_list : list = [faker.name() for i in range(10)]
        fake_score_list : list = [random.randint(80,100) for i in range(10)]
        fake_email_list : list = [faker.email() for i in range(10)]

        faker_dict['fake_name_list'] : list = fake_name_list
        faker_dict['fake_score_list'] : list = fake_score_list
        faker_dict['fake_email_list'] : list = fake_email_list
        return faker_dict

class Xlsx:
    def save_data(self,targetData:Union[dict,list])-> None:
        """ Pandas로 데이터 저장 """
        savePath : str = os.path.abspath('fake_data')
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        
        fileName : str = os.path.join(savePath,'fake.xlsx')

        # 데이터 
        name_list : list = targetData['fake_name_list']
        score_list : list = targetData['fake_score_list']
        email_list : list = targetData['fake_email_list']

        # 판다스로 데이터 저장
        df = pd.DataFrame(
            {
                '이름' : name_list,
                '점수' : score_list,
                '이메일' : email_list   
            }
        )

        df.to_excel(fileName)
        print(f'{fileName} 파일 저장완료!\n')

    def load_data(self,srcFile:str)-> dict:
        """ Pandas로 데이터 로드 """
        df_from_excel = pd.read_excel(srcFile)

        data : dict = dict()

        name_list : list =  df_from_excel['이름'].tolist()
        score_list : list =  df_from_excel['점수'].tolist()
        email_list : list =  df_from_excel['이메일'].tolist()
        
        data['name_list'] = name_list
        data['score_list'] = score_list
        data['email_list'] = email_list
        return data

class SendEmail:    
    def __init__(self) -> None:
        self._secrets = get_secrets(key='SECRET')

    def send(self,data_list:Union[dict,list])-> None:
        name_list : list = data_list['name_list']
        score_list : list = data_list['score_list']
        email_list : list = data_list['email_list']

        for i in range(len(name_list)):
            name  : str = name_list[i]
            score : int = score_list[i]
            email : str = email_list[i]
            with smtplib.SMTP(self._secrets['smtp_server'],self._secrets['smtp_port']) as server :                
                # TLS 보안 연결
                server.starttls()

                # 로그인
                server.login(self._secrets['smtp_user_id'],self._secrets['smtp_user_pw'])

                # 텍스트 메시지            
                text = f'{name} 님의 점수 는 {score} 점 입니다.'

                # 메일 객체 생성하기 : 메시지 내용에는 한글이 들어가기 때문에 UTF-8 사용
                msg = MIMEText(_text=text,_charset='utf-8')

                # 메일 제목
                msg['Subject'] = f'{name} 님의 점수 결과입니다'    

                # 송신자
                msg['From'] = 'yshrim12@naver.com'
                
                # 수신자
                msg['To'] = email

                # 로그인된 서버에 이메일 전송
                response = server.sendmail(from_addr=msg['From'],to_addrs=msg['To'],msg=msg.as_string())

                # 이메일 전송 성공일 시 빈 값 반환
                if not response:
                    print(f'{msg["To"]} - 이메일 전송 완료!\n')
                else:
                    print(response)        

def main()-> None:
    # Faker Instance
    faker = FakerData()

    # Create Faker Data
    faker_data : dict = faker.create_faker_data()
    
    # Xlsx Instance
    xlsx = Xlsx()

    # 데이터 저장하기
    xlsx.save_data(targetData=faker_data)

    # 데이터 읽어오기
    data_list : dict = xlsx.load_data(srcFile='fake_data/fake.xlsx')

    # SendEmail Instance
    sendMail = SendEmail()

    # 이메일 전송하기
    sendMail.send(data_list=data_list)

if __name__ == '__main__':
    main() 