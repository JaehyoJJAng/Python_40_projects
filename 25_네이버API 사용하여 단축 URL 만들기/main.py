from config.config import get_api_secrets
from typing import Dict
import urllib.parse
import urllib.request
import json
import tkinter
from tkinter import *

_headers : Dict[str,str] = get_api_secrets(key='headers')        
class GUI:
    def __init__(self) -> None:
        self.window = tkinter.Tk()

        self.api_request_url : str = 'https://openapi.naver.com/v1/util/shorturl'

    def run(self)-> None:
        """ GUI 세팅 """
        #tkinter 윈도우설정
        self.window.title("단축 URL")
        self.window.geometry("500x200+800+300")
        self.window.resizable(False, False)

        #라벨
        self.lb1_text = Label(self.window,width=10,text="url입력:")
        self.lb1_text.grid(row=0, column=0)

        #URL 입력
        self.entry_url = Entry(self.window,width=20)
        self.entry_url.grid(row=0, column=1,pady=10)

        # URL 초기화 버튼
        self.btn_url_clear = tkinter.Button(self.window, overrelief="solid",text="URL 초기화", width=5,
                                command=self.btn_clear_url, repeatdelay=1000, repeatinterval=100)
        self.btn_url_clear.grid(row=0, column=3,padx=5)

        #실행버튼
        self.btn_ok = tkinter.Button(self.window, overrelief="solid",text="실행", width=5,
                                command=self.btn_shorturl_click, repeatdelay=1000, repeatinterval=100)
        self.btn_ok.grid(row=0, column=2,padx=5)

        # 검색 초기화 버튼
        self.btn_entry_result_clear = tkinter.Button(self.window, overrelief="solid",text="결과 초기화", width=5,
                                command=self.btn_clear_entry_result, repeatdelay=1000, repeatinterval=100)
        self.btn_entry_result_clear.grid(row=1, column=3,padx=5)

        #라벨
        self.lb2_text = Label(self.window,width=10,text="결과:")
        self.lb2_text.grid(row=1, column=0)

        #URL 결과
        self.entry_result = Entry(self.window,width=28)
        self.entry_result.grid(row=1, column=1, columnspan=2,pady=5)

        # tkinter 메인루프 실행
        self.window.mainloop()

    def btn_shorturl_click(self)-> None:
        """ shorturl 클릭 시 이벤트 메소드 """
        my_url : str = self.entry_url.get()

        short_url : str = self.get_naver_shorturl(long_url=my_url)

        self.entry_result.delete(0,'end')
        self.entry_result.insert(0,short_url)

    def get_naver_shorturl(self,long_url:str)-> str:
        """ Short URL 생성 메소드 """
        encText : str = urllib.parse.quote_plus(long_url)
        data : str = f'url={encText}'

        request = urllib.request.Request(self.api_request_url)
        request.add_header('X-Naver-Client-Id',_headers['X-Naver-Client-Id'])
        request.add_header('X-Naver-Client-Secret',_headers['X-Naver-Client-Secret'])

        response = urllib.request.urlopen(request,data=data.encode('utf-8'))
        rescode : int = response.getcode()
        
        if (rescode == 200):
            response_body : bytes = response.read()
            decode_json : dict = json.loads(response_body.decode('utf-8'))
            return decode_json['result']['url']
        else:
            return f'Error Code : {rescode}'
    
    def btn_clear_entry_result(self):
        """ 결과 텍스트 초기화 버튼 클릭 시 이벤트 메소드"""
        self.entry_result.delete(0,'end')

    def btn_clear_url(self):
        """ 입력 URL 초기화 """
        self.entry_url.delete(0,'end')
        
def main()-> None:
    gui = GUI()

    gui.run()

if __name__ == '__main__':
    main()