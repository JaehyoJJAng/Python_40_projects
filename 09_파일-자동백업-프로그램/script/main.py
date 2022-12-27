from distutils.dir_util import copy_tree
import os
import sys
# from win10toast import ToasNotifier

class WindowEvent:
    def window_alarm(self,srcDir:str,dstDir:str):
        pass
        # toaster = ToastNotifier()
        # toaster.show_toast('백업이 완료되었습니다',f'{srcDir} >>> {dstDir}',duration=5) # 윈도우에 알림을 5초 동안 발생 시킴

class Util:
    def __init__(self):
        # Window Instance
        self.window = WindowEvent()
    @staticmethod
    def folder_check(Dir:str)-> None:
        """ Directory Exists """
        if not os.path.exists(Dir):
            print("디렉토리가 존재하지 않습니다!")
            sys.exit()

    def folder_backup(self,srcDir:str,dstDir:str)-> None:
        """ Folder Backup Method """
        # 디렉토리 체크
        self.folder_check(Dir=srcDir)
        self.folder_check(Dir=dstDir)

        # 백업 받을 폴더가 존재하지 않는 경우 새로 생성
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)

        """ 폴더 백업 메소드 """
        result = copy_tree(srcDir,dstDir,update=1)

        self.window.window_alarm(srcDir=srcDir,dstDir=dstDir)

def main():
    # Util Instance
    util = Util()

    # Source Dir
    srcDir = '../source/'

    # Destination Dir
    dstDir = '../backup'

if __name__ == '__main__':
    main()