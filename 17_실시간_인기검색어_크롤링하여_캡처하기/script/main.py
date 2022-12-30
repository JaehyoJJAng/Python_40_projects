from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

class ChromeDriver:
    @staticmethod
    def return_driver():
        # options 객체
        chrome_options = Options()

        # headless Chrome 선언
        chrome_options.add_argument('--headless')

        # 브라우저 꺼짐 방지
        chrome_options.add_experimental_option('detach', True)

        # 불필요한 에러메시지 없애기
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        return browser
    
class Crawl:
    def __init__(self) -> None:
        self.browser = ChromeDriver().return_driver()
        
        self.url : str = 'https://www.signal.bz/news'
    
    def get_items(self)-> list:
        """ 실시간 검색어 추출 """
        # URL 접속
        self.browser.get(url=self.url)

        # item length 추출
        item_length : int = len(self.browser.find_elements(By.CSS_SELECTOR,'a.rank-layer'))
        
        item_list : list = []
        for idx in range(item_length):
            item_dic : dict = {}

            items : list = self.browser.find_elements(By.CSS_SELECTOR,'a.rank-layer')

            title : str = items[idx].find_element(By.CSS_SELECTOR,'.rank-text').text.strip()
            link  : str = items[idx].get_attribute('href')

            item_dic['title'] = title
            item_dic['link']  = link
            item_list.append(item_dic)
        return item_list

    def website_capture(self,items:list):
        """ 추출한 link로 접속 후 캡쳐 파일 저장 """
        savePath = '../capture'
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        
        for count,item in enumerate(items,1):
            print(item['title'],item['link'])

            # 실시간 검색어 링크로 이동
            self.browser.get(url=item['link'])

            # 로딩 대기시간
            self.browser.implicitly_wait(time_to_wait=10)

            self.browser.save_screenshot(os.path.join(savePath,str(count) + '_' + item['title'] + '.png'))
            print(f'{count}_{item["title"]}.png 캡처 완료!\n')

def main():
    crawl = Crawl()

    items : list = crawl.get_items()

    crawl.website_capture(items=items)    

if __name__ == '__main__':
    main()