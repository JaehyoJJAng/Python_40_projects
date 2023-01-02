from glob import glob
from typing import List,Dict,Union
from PIL import Image , ImageDraw , ImageFont
import os

class Util:
    def load_image_path(self,imgPath:str)-> Dict[str,Union[List[str],str]]:
        """ 이미지 파일 경로 가져오기 """
        dstPath = '워터마크이미지'
        if not os.path.exists(dstPath):
            os.mkdir(dstPath)

        # 워터마크이미지 폴더로 파일 경로 변경
        img_list : List[str] = glob(f"{imgPath}/*.jpeg")
        img_info : Dict[str,Union[List[str],str]] = {'img_list':img_list,'dstPath':dstPath}
        return img_info
    
    def add_water_mark(self,img_info:Dict[str,Union[List[str],str]])-> None:
        """ 이미지에 워터마크 넣기 """
        dstPath : str = img_info['dstPath']
        img_list : List[str] = img_info['img_list']

        for img in img_list:
            # Destination File
            dstFile : str = os.path.join(dstPath,str(img).split('/')[-1])

            image = Image.open(img)        
            width , height = image.size

            draw = ImageDraw.Draw(image)
            text = 'JaehyoJJAng <두식이>'

            font = ImageFont.truetype('font/KyoboHandwriting2021sjy.otf',70)
            tw , th = font.getsize(text=text)

            x = int((width/2) - (tw/2))
            y = int((height/2) - (th/2))

            draw.text((x,y),text=text,font=font)
            image.save(dstFile)
            
            print(f'변환완료 : {img} - {dstFile}')

def main()-> None:
    # Util Instance
    util = Util()

    # 이미지 파일 가져오기
    img_info : Dict[str,Union[List[str],str]] = util.load_image_path(imgPath='원본이미지/')

    # 이미지에 워터마크 삽입
    util.add_water_mark(img_info=img_info)

if __name__  == '__main__':
    main()