import imaplib
import email
from email import policy
from config.config import get_secrets   
# from win10toast import ToastNotifier

class Naver:
    def __init__(self) -> None:
        self.naver_email = NaverEmail()

class NaverEmail:
    def __init__(self) -> None:
        self._secrets : dict = get_secrets(key='SECRET')
    
    def load_recent_email(self)-> list:
        imap = imaplib.IMAP4_SSL('imap.naver.com')

        _id : str = self._secrets['smtp_user_id']
        _pw : str = self._secrets['smtp_user_pw']
        
        # imap Login
        imap.login(_id,_pw)

        imap.select('INBOX')

        resp , data = imap.uid('search',None,'All')
        
        all_eamil = data[0].split()
        last_email = all_eamil[-5:]
        
        save_data : list = list()
        for mail in reversed(last_email):
            data_dic : dict = dict()

            result,data = imap.uid('fetch',mail,'(RFC822)')
            
            # Raw Email
            raw_eamil = data[0][1]
            
            # Email Messages
            email_message = email.message_from_bytes(raw_eamil,policy=policy.default)
            
            # From
            From = email_message["From"]

            # sender
            sender = email_message['Sender']

            # To
            to = email_message['To']

            # date
            date = email_message['Date']

            # Subject
            subject = email_message['Subject']

            # Message
            message = ''
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    if part.get_content_type() == 'text/plain':
                        bytes = part.get_payload(decode=True)
                        encode = part.get_content_charset()
                        message = message + str(bytes,encode)

            data_dic['from'] = From
            data_dic['sender'] = sender
            data_dic['to'] = to
            data_dic['date'] = date
            data_dic['subject'] = subject
            data_dic['message'] = message
            save_data.append(data_dic)
            
        imap.close()
        imap.logout()

        return save_data

class WindowAlarm:
    def alarm(self,data_list : list):
        toast = ToastNotifier()

        send_list = []
        while True:
            print('메일 검사')
            # if 제목.find('입금') >= 0:
                # if 제목 not in send_list:
                    # send_list.append(제목)
                    # toaster.show_toast(f'중요 메일이 도착했습니다\n{제목}',duration=10)

def main()-> None:
    # Naver Instance
    naver = Naver()
    
    # 네이버 최근 이메일 조회하기
    data_list : list = naver.naver_email.load_recent_email()

    # 윈도우 알람
    winalarm = WindowAlarm()

    winalarm.alarm(data_list=data_list)

if __name__ == '__main__':
    main()