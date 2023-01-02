from gtts import gTTS
from playsound import playsound
import os
import sys 
import tkinter
import tkinter.font
from tkinter import *
import tkinter.ttk
import threading
import time
from typing import List


class Sound:
    def text_to_sound(self,text:str)-> None:
        soundPath : str = 'sound/'
        fileName  : str = f'{text.split()[0]}.mp3'
        if not os.path.exists(soundPath):
            os.mkdir(soundPath)

        try :
            tts = gTTS(text=text,lang='ko')
            tts.save(os.path.join(soundPath,fileName))
        except:
            print('사운드 파일저장 실패!')
            sys.exit()

        try :
            playsound(os.path.join(soundPath,fileName))
        except Exception as e:
            print(f'음성 재생 실패!\n')
            sys.exit()

def main()-> None:
    # Sound Instance
    sound = Sound()
    
    # Sound Execute
    sound.text_to_sound(text='스트레칭 하세요')
    
if __name__ == '__main__':
    main()