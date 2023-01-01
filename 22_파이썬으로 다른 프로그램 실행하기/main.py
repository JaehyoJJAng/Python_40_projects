""" 맥북에서는 os.start 명령어 실행 불가함 """
import os

class Util:
    def os_startfile(self, filePath: str) -> None:
        """ os.startfile의 기능을 이용하여 윈도우의 파일 실행하기 """
        os.startfile(filePath)

def main():
    # Util Instance
    util = Util()

    # 윈도우 파일 실행하기
    util.os_startfile(filePath='txt/test.txt')

if __name__ == '__main__':
    main()


