""" 맥북에서는 os.start 명령어 실행 불가함 """
import os
import subprocess
import time
import schedule

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

    def execute_other_py(self):
        """ 다른 파이썬 파일 실행
        ! script - print_hello.py 파일 생성 후 아래 코드 실행하도록 함 """
        script: str = 'script/print_hello.py'
        subprocess.call(f'python3 {script}', shell=True)
        print(f'{script} - 실행완료')

    def manage_schedule(self):
        """ 일정 관리하여 다른 프로그램 실행하기 """
        schedule.every(3).seconds.do(self.do_file_backup)

        while True:
            schedule.run_pending()
            time.sleep(1.0)

    def do_file_backup(self):
        """ 파일 백업 코드 - self.manage_schedule 메소드와 연계 """

        # 백업 대상 파일
        src_file: str = 'main.py'

        # 백업 경로 없으면 생성
        back_path: str = 'backup'
        if not os.path.exists(back_path):
            os.mkdir(back_path)

        # 백업 파일 이름
        back_file_name: str = os.path.join(back_path, f'{src_file}.bak')

        # 백업 코드
        backup_command: str = f'cp -R {src_file} {back_file_name}'

        # 커맨드 실행하기
        subprocess.call(backup_command, shell=True)
        print('백업 프로그램 실행 완료!')
        
def main():
    # Util Instance
    util = Util()

    # 윈도우 파일 실행하기
    util.os_startfile(filePath='txt/test.txt')

    # 윈도우 응용 프로그램 실행하기
    util.execute_app()

    # 다른 파이썬 파일 실행하기
    util.execute_other_py()

    # 일정 관리하여 다른 프로그램 실행하기
    util.manage_schedule()

if __name__ == '__main__':
    main()


