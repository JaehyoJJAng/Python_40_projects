from PIL import Image , ImageDraw , ImageFont
import os
from typing import Dict

class Draw:
    def draw_empty_file(self,worker_name:str,text:str)-> None:
        """ 빈 이미지 파일 만들고 글 쓰는 메소드 """
        filePath : str = 'a4'
        fileName : str = os.path.join(filePath,f'{worker_name}.png')
        if not os.path.exists(filePath):
            os.mkdir(filePath)

        empty_im = Image.new('RGB',(2480,3508),'white')

        draw = ImageDraw.Draw(empty_im)
        draw.text(
            (300,300),
            text=text,
            font=ImageFont.truetype('font/KyoboHandwriting2021sjy.otf',60),
            fill=(0,0,0))
        
        try :
            empty_im.save(fileName)
            print(f'이미지 파일 생성완료!\n{fileName}')
        except Exception as e :
            print(f'이미지 파일 생성 실패!\n{e}')

class EmploymentContract:
    def __init__(self,draw)-> None:
        self.draw = draw

    def write_in_file(self,worker_info:Dict[str,str])-> None:
        """ 근로계약서 자동으로 작성하는 메소드 """
        text = f"""

                                  근로계약서



파이썬커피(이하"사업주"라 함)과(와) {worker_info['worker_name']}(이하"근로자"라 함)은
다음과 같이 근로계약을 체결한다.
1. 근로계약기간 : {worker_info['work_date']}
  ※ 근로계약기간을 정하지 않는 경우에는 “근로개시일”만 기재
2. 근 무 장 소 : 서울시 파이썬커피
3. 업무의 내용 : 음료 제조, 디저트 제조, 포스 업무, 매장정리, 청소
4. 소정근로시간 :    시   분부터    시   분까지 (휴게시간 :  시  분~  시   분)
5. 근무일/휴일 : 매주   일(또는 매일단위)근무, 주휴일 매주   요일
6. 임  금
  - 월(일, 시간)급 :                    원
  - 상여금 : 있음 (    )                           원,  없음 (     )
  - 기타급여(제수당 등) : 있음 (    ),   없음 (    )
    ·                          원,                                 원
    ·                          원,                                 원
  - 임금지급일 : 매월(매주 또는 매일)       일(휴일의 경우는 전일 지급)
  - 지급방법 : 근로자에게 직접지급(    ),  근로자 명의 예금통장에 입금(    )
7. 연차유급휴가
  - 연차유급휴가는 근로기준법에서 정하는 바에 따라 부여함
8. 사회보험 적용여부(해당란에 체크)
  □ 고용보험  □ 산재보험  □ 국민연금  □ 건강보험
9. 근로계약서 교부
  - 사업주는 근로계약을 체결함과 동시에 본 계약서를 사본하여 근로자의
    교부요구와 관계없이 근로자에게 교부함(근로기준법 제17조 이행)
10. 기  타
  - 이 계약에 정함이 없는 사항은 근로기준법령에 의함

                                     년      월      일


(사업주) 사업체명 :  파이썬커피   (전화 : 02-123-4567   )
        주    소 :  서울시 파이썬커피
        대 표 자 :    김파이   (서명)

(근로자) 주    소 :
        연 락 처 :
        성    명 :     {worker_info['worker_name']}  (서명)
"""
        # 위 텍스트를 파일로 만들기
        self.draw.draw_empty_file(worker_name=worker_info['worker_name'],text=text)

def main():
    # DrawA4 Instance
    draw = Draw()
    
    # Worker Info
    worker_info : Dict[str,str] = {'worker_name':'이재효','work_date':'2023.1.1 ~ 2023.12.30'}

    # EmploymentContract Instance
    EC = EmploymentContract(draw=draw)
    EC.write_in_file(worker_info=worker_info)

if __name__ == '__main__':
    main()