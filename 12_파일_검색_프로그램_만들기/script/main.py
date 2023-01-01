import os
from datetime import datetime
from typing import List,Dict,Union

class FoundFiles:
    def __init__(self,dstPath:str) -> None:
        self.dstPath : str = dstPath
    
    def found_ext(self)-> List[Dict[any,any]]:
        """ 폴더에서 엑셀과 워드 파일을 찾아 리턴 """
        found_list : list = []
        for (path,dir,files) in os.walk(self.dstPath):
            for filename in files:
                file_dict : dict = dict()

                # os.path.splittext() : 파일명과 확장자명을 튜플 자료형으로 반환 ('파일명','확장자명')
                file , ext = (os.path.splitext(filename))
                if ext == '.xlsx' or ext == '.docx':
                    file_dict['file'] = f'{path}/{filename}'
                    found_list.append(file_dict)
        return found_list

    def print_file_info(self,found_list:list)-> List[Dict[str,str]]:
        """ 파일 상세 정보 리턴 """
        file_infos : list = []
        for found in found_list:
            info_data : dict = dict()

            # 파일명
            file = found['file']
            
            # 파일 만든 시간
            ctime = os.path.getctime(file)

            # 파일 수정 시간
            mtime = os.path.getmtime(file)
            
            # 파일 마지막 엑세스 시간
            atime = os.path.getatime(file)
            
            # 파일 사이즈
            file_size = os.path.getsize(file)
            
            info_data['file']  = file
            info_data['ctime'] = ctime
            info_data['mtime'] = mtime
            info_data['atime'] = atime
            info_data['file_size'] = file_size
            file_infos.append(info_data)
        return file_infos

    def check_date_file(self,file_infos:list)-> List[str]:
        """ 최근 생성된 파일 찾아 리턴 """
        recent_files = []
        for file_info in file_infos:
            file = file_info['file']
            mtime = file_info['mtime']

            # 현재시간 - 파일생성 시간으로 파일이 생성된 날짜 계산 
            days = datetime.now() - datetime.fromtimestamp(mtime)

            # 생성된 시간이 5일 이내에 생성된 파일만 출력
            if days.days <= 5:
                file_info['file'] = file
                recent_files.append(file_info)
        return recent_files

    def check_size_file(self,recent_files:list)-> List[int]:
        """ 파일 용량이 10KBytes를 넘는 파일만 리턴 """
        kbyte_files : list = []
        for recent_file in recent_files:
            file_size = recent_file['file_size']
            if file_size > 10000:
                kbyte_files.append(recent_file)
        return kbyte_files

def main()-> None:
    dstPath = '../utils'
    founds = FoundFiles(dstPath=dstPath)

    # 파일 찾기
    found_list : list = founds.found_ext()
    
    # 파일 상세정보
    file_infos : list = founds.print_file_info(found_list=found_list)

    # 최근 생성된 파일
    recent_files : list = founds.check_date_file(file_infos=file_infos)

    # 용량 10KBytes를 넘는 파일
    kbyte_files : list = founds.check_size_file(recent_files=recent_files)
    
if __name__ == '__main__':
    main()