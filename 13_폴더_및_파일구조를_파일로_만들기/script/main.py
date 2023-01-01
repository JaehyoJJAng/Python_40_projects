import os
import seedir as sd
from typing import List,Dict

class Util:
    def load_path_files(self,srcPath:str)-> List[Dict[str,str]]:
        """ 폴더 안의 모든 파일 읽어오기 """
        file_list = []
        for (path,dir,files) in os.walk(srcPath):
            fileInfo = dict()

            fileInfo['path'] = path
            fileInfo['dir']  = dir
            fileInfo['files'] = files
            file_list.append(fileInfo)
        return file_list
    
    def print_tree(self,srcPath:str)-> None:
        """ 폴더 트리 구조 출력 """
        sd.seedir(srcPath,style='emoji')

    def print_check_regex(self,srcPath:str,ext:str)-> any:
        """ 파이썬 파일만 찾아 폴더트리 구조 출력"""
        dir_tree = sd.seedir(srcPath,printout=False,include_files=ext,regex=True,style='emoji')

        return dir_tree

    def save_file(self,dir_tree)-> None:
        """ Dir Tree 텍스트 파일로 저장 """
        savePath = os.path.abspath('dir_tree')
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        fileName = os.path.join(savePath,'tree.txt')
        with open(fileName,'w',encoding='UTF-8') as fp:
            fp.write(dir_tree)
def main()-> None: 
    srcPath = '../'
    
    # Util Instance
    util = Util()

    # 폴더 안 모든 파일 읽어오기
    file_list : list = util.load_path_files(srcPath=srcPath)

    # 폴더 트리 출력
    util.print_tree(srcPath=srcPath)

    # 파이썬 파일만 찾아 폴더트리 구조 출력
    dir_tree : any = util.print_check_regex(srcPath=srcPath,ext='.*\.py')

    util.save_file(dir_tree=dir_tree)

if __name__ == '__main__':
    main()