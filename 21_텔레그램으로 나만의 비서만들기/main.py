from config.config import get_telegram_secret
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import telegram
import os
import datetime
import urllib.parse as rep
import datetime

class ChromeDriver:
    @staticmethod
    def set_driver():
        """ Create Chrome Driver Instance and Return """
        # options 객체
        chrome_options = Options()

        # headless Chrome 선언
        chrome_options.add_argument('--headless')

        # 브라우저 꺼짐 방지
        chrome_options.add_experimental_option('detach', True)

        # Add Header
        chrome_options.add_argument(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Whale/3.13.131.36 Safari/537.36")

        # 불필요한 에러메시지 없애기
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Chrome 객체 받아오기
        browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

        # 브라우저 크기 최대화
        browser.maximize_window()

        # browser 리턴
        return browser

class NewsCapture:
    def __init__(self) -> None:
        self.browser = ChromeDriver().set_driver()
    
    @staticmethod
    def make_save_folder(imgPath:str,keyword:str)-> str:
        if not os.path.exists(imgPath):
            os.mkdir(imgPath)
        
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        fileName : str = str(os.path.join(imgPath,str(now) + '_' + keyword + '.png'))
        return fileName        

    def capture(self,keyword:str)-> str:
        """ 뉴스 캡쳐 """
        url : str = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={rep.quote_plus(keyword)}'
        
        # URL 이동
        self.browser.get(url=url)
        self.browser.implicitly_wait(time_to_wait=10)

        # 파일 저장 경로 생성
        fileName : str = self.make_save_folder(imgPath='capture/',keyword=keyword)

        # 캡쳐 파일 저장하기
        self.browser.save_screenshot(filename=fileName)

        return fileName

class Telegram:
    def __init__(self) -> None:
        self._token = get_telegram_secret(key='token')
        self._chatid = get_telegram_secret(key='chatid')
    
    def create_telegram_bot(self)-> None:
        """ Telegram Bot 인스턴스 생성 """
        try:
            self.bot = telegram.Bot(token=self._token)
            print('텔레그램 봇 인스턴스가 생성되었습니다\n')
        except:
            print('텔레그램 봇 인스턴스 생성에 실패하였습니다')
            raise NameError

    def send_message(self,message:str)-> None:
        """ 메시지 보내기 """
        try :
            if message:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                self.bot.sendMessage(chat_id=self._chatid,text=message)
                print(f'{now}\n텔레그램 포토 메시지 전송 성공!\n')
            else:
                self.bot.sendMessage(chat_id=self._chatid,text="You don't have any massages")
                print('텔레그램 메시지 전송 실패!')
        except Exception as e:
            print(e)
    
    def send_photo_message(self,photo):
        """ 포토 메시지 보내기 """
        try :
            if photo:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                self.bot.sendPhoto(chat_id=self._chatid,photo=open(photo,'rb'),caption=photo)
                print(f'{now}\n텔레그램 포토 메시지 전송 성공!\n')
            else:
                self.bot.sendMessage(chat_id=self._chatid,text="You don't have any photos")
                print('텔레그램 포토 메시지 전송 실패!')
        except Exception as e:
            print(e)

def main():
    # Telegram Instance
    tele = Telegram()

    # Telegram 클래스에 Bot 인스턴스 생성하기
    tele.create_telegram_bot()

    # NewsCapture Instance
    newsCap = NewsCapture()

    # 뉴스 캡쳐하기
    fileName : str = newsCap.capture(keyword='날씨')

    # 텔레그램 포토 메시지 보내기
    tele.send_photo_message(photo=fileName)
    
if __name__ == '__main__':
    main()