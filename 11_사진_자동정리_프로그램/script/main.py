from PIL import Image
from PIL.ExifTags import TAGS
from glob import glob
from geopy import Nominatim
import os

class Pictures:
    def __init__(self,picturePath:str)-> None:
        self.picturePath = picturePath

    def get_picture_info(self)-> list:
        """ 사진 파일의 정보 추출 """
        # 사진 파일들 가져오기
        pictures : list = glob(f'{self.picturePath}/*.jpg')

        pictures_data_list : list = []
        for picture in pictures:
            image = Image.open(picture)
            info = image.getexif()
            image.close()

            # 데이터를 키:값 으로 담겨줄 딕셔너리 변수 선언
            taglabel : dict = {}
            for tag , value in info.items():
                decoded = TAGS.get(tag,tag)
                taglabel[decoded] = value

            # 딕셔너리에 데이터 다 추가한 후 리스트 변수에 추가
            pictures_data_list.append(taglabel)

        # 추출 데이터 리턴
        return pictures_data_list

    def convert_coodi_to_address(self,pic_datas:list)-> None:
        """ 좌표 데이터를 주소 데이터로 변환 """
        geolocoder = Nominatim(user_agent='South Korea',timeout=None)
        address = geolocoder.reverse('36.77384887777778, 127.040708697222223') # lat_lng_str
        address_list = address[0].split(',')

        area = address_list[2].strip() + '_' + address_list[1].strip()

def main():
    # 사진 있는 경로
    pictures : str = '../Pictures'

    # Pictures Instance
    pic = Pictures(picturePath=pictures)

    # 사진 정보 추출하기 [리스트]
    pic_datas : list = pic.get_picture_info()

if __name__ == '__main__':
    main()