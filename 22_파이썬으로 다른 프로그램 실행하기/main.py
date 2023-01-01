""" 맥북에서는 os.start 명령어 실행 불가함 """
import os
import subprocess
import time

class Util:
    def os_startfile(self, filePath: str) -> None:
        """ os.startfile의 기능을 이용하여 윈도우의 파일 실행하기 """
        os.startfile(filePath)

    def execute_app(self) -> None:
        """ 윈도우의 응용 프로그램 실행하고 종료 """
        memo_process = subprocess.Popen('notepad')
        time.sleep(5)

        if memo_process.poll() == None:
            print('메모장을 종료합니다')
            memo_process.kill()

def main():
    # Util Instance
    util = Util()

    # 윈도우 파일 실행하기
    util.os_startfile(filePath='txt/test.txt')

    # 윈도우 응용 프로그램 실행하기
    util.execute_app()

if __name__ == '__main__':
    main()


