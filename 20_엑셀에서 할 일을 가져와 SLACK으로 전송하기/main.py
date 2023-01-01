import requests as rq
import json
from config.config import get_webhook_url
import datetime
import pandas as pd
from glob import glob
import time
from typing import Dict,List,Union

class Slack:
    def __init__(self,webhook_url:str) -> None:
        self.webhook_url = webhook_url

    @staticmethod
    def send_post(webhook_url:str,headers:dict,data:dict)-> None:
        """ send post data to slack (waytothem channel) """
        with rq.Session() as session:
            with session.post(webhook_url,headers=headers,data=json.dumps(data)) as response :
                return response

    def send_slack_webhook(self,strText:str)-> None:
        """ Send a Message Using Slack """
        # Headers
        headers = {"Content-type": "application/json"}

        # Send Data To Waytothem Channel 
        data = {"text": strText}

        # Send data to slack && response status check
        response = self.send_post(webhook_url=self.webhook_url,headers=headers,data=data)
        if response.ok:
            print('ok')
        else:
            print('error')

class Xlsx:
    def load_data(self,filePath:str)-> Dict[str,List[Union[str,int]]]:
        """ 데이터 읽어오기 """
        # 데이터 담을 딕셔너리 선언
        data_dic : dict = dict()

        # Read data in xlsx
        df_from_excel = pd.read_excel(filePath)

        time_list : list = df_from_excel['시간'].to_list()
        todo_list : list = df_from_excel['할일'].to_list()
        
        data_dic['time_list'] = time_list
        data_dic['todo_list'] = todo_list
        return data_dic

    def time_check(self,data_dic:dict,slack)-> None:
        # Now Time
        now = datetime.datetime.now()
        
        time_list : list = data_dic['time_list']
        todo_list : list = data_dic['todo_list']

        for i , t in enumerate(time_list):
            time_difference = t - now
            time_difference_seconds = time_difference.seconds
            time_difference_day = time_difference.days
            
            print(todo_list[i],time_difference_seconds)
            if time_difference_day >= 0 and time_difference_seconds <= 60:
                print(todo_list[i],'메시지 전송!')
                # 슬랙에 메시지 전송
                slack.send_slack_webhook(strText=todo_list[i])
                # 타임 대기
                time.sleep(61.0)            
        time.sleep(1.0)
def main()-> None:
    # Xlsx Instance
    xlsx = Xlsx()

    # Load Data in xlsx
    data_dic : dict = xlsx.load_data(filePath=glob('todolist/*.xlsx')[0])

    # Slack Instance
    slack = Slack(webhook_url=get_webhook_url(key='url'))

    # Slack Message
    xlsx.time_check(data_dic=data_dic,slack=slack)

if __name__ == '__main__':
    main()