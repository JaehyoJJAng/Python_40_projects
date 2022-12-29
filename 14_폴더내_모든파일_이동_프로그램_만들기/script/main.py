import os
import shutil

class Util:
    def check_dir_exist(self,dir:str)-> None:
        if not os.path.exists(dir):
            os.mkdir(dir)

    def src_to_dst(self,srcPath:str,dstPath:str)-> None:
        for (path,dir,files) in os.walk(srcPath):
            for file in files:
                addPath = os.path.join(path,file)
                
                try :
                    # srcPath Files -> dstPath Files
                    shutil.move(addPath,dstPath)
                    print(f'{addPath} ==> {dstPath}')
                except:
                    pass

def main()-> None:
    srcPath : str = '../utils'
    dstPath : str = '../dst'

    # Util Instance
    util = Util()
    
    # dir Check
    util.check_dir_exist(dir=dstPath)

    # 파일 이동
    util.src_to_dst(srcPath=srcPath,dstPath=dstPath)

if __name__ == '__main__':
    main()