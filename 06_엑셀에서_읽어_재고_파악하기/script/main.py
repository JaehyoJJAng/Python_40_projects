import os.path

import pandas as pd
import glob

class Xlsx:
    def __init__(self,xlsxFiles:list):
        self.xlsxFiles : list = xlsxFiles

    def load_file(self)-> any:
        """ 엑셀 파일 읽어오는 메소드 """
        merge_df = pd.DataFrame()
        for file in self.xlsxFiles:
            df_from_excel = pd.read_excel(file)

            # 재고위치 라는 새로운 키에 다음과 같은 Value를 대입
            df_from_excel['재고위치'] = str(file).split('_')[-1].split('.')[0]

            # 엑셀에서 읽은 데이터프레임을 merge_df 에 추가
            merge_df = pd.concat([merge_df,df_from_excel])

        return merge_df

    def check_date(self,merge_df)-> any:
        """ 특정 날짜의 재고 파악하는 메소드 """

        # 특정 날짜 이전의 재고 파악
        filter_df = merge_df[merge_df['날짜'] < '2015-01-01']

        # 특정 기간의 재고 파악
        filter_df = merge_df[merge_df['날짜'].between('2012-1-1','2015-12-31')]

        # 특정 기간의 재고수량이 15개 미만일 경우 엑셀로 저장
        filter_df = merge_df[merge_df['날짜'].between('2012-1-1','2015-12-31')]
        filter_df = filter_df[filter_df['수량'] < 15]

        return filter_df

    def save_xlsx(self,filter_df)-> None:
        """ 추출된 재고데이터 새로운 파일로 저장하는 메소드 """
        savePath = '../result'
        fileName = os.path.join(savePath,'날짜_수량.xlsx')
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        try :
            filter_df.to_excel(fileName)
            print(f"{fileName} - 파일 저장 완료!")
        except Exception as e:
            print(f"{e}\n\n파일 저장 실패!")

def main():
    xlsxFiles : list = glob.glob(os.path.join('../xlsx','*.xlsx'))

    # Create Xlsx Instance
    xlsx = Xlsx(xlsxFiles=xlsxFiles)

    # 엑셀 파일 읽어오기
    merge_df : any = xlsx.load_file()

    # 특정 날짜 이전의 재고 파악하기
    filter_df : any = xlsx.check_date(merge_df=merge_df)

    # 파일로 저장
    xlsx.save_xlsx(filter_df=filter_df)

if __name__ == '__main__':
    main()

