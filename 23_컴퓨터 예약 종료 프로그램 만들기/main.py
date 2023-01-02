import os
import time
import tkinter
from tkinter import *
import tkinter.ttk
from typing import List

class GUI:
    def __init__(self) -> None:
        self.window = tkinter.Tk()

    def main(self) -> None:
        self.window.title('컴퓨터 전원 끄기')
        self.window.geometry('1024x800+600+200')
        self.window.resizable(False, False)

        lb_hour = Label(self.window, width=10, text='시간:')
        lb_hour.grid(row=0, column=0)

        time_values: List[str] = [str(i) + '시간' for i in range(0, 24)]
        time_combobox = tkinter.ttk.Combobox(
            self.window, width=10, height=10, values=time_values)
        time_combobox.grid(row=0, column=1, pady=5)
        time_combobox.set(time_values[0])

        lb_min = Label(self.window, width=10, text="  분:")
        lb_min.grid(row=1, column=0)

        min_values : List[str] = [str(i)+"분" for i in range(0, 60)]
        min_combobox = tkinter.ttk.Combobox(
            self.window, width=10, height=10, values=min_values)
        min_combobox.grid(row=1, column=1, pady=5)
        min_combobox.set(min_values[30])

        self.window.mainloop()

    def btn_action(self) -> None:
        """ 실행 버튼 """
        btn_action = tkinter.Button(self.window, overrelief="solid", text="실행", width=10,command=btn_action, repeatdelay=1000, repeatinterval=100)
        btn_action.grid(sticky=N + E + S + W, row=4, columnspan=3, padx=10, pady=5)

    def btn_cancer(self) -> None:
        """ 취소 버튼 """
        btn_cancer = tkinter.Button(self.window, overrelief="solid",text="취소", width=10,command=btn_cancer, repeatdelay=1000, repeatinterval=100)
        btn_cancer.grid(sticky = N + E + S + W,row=5,columnspan=3,padx=10,pady=5)

    def shutdown(self) -> None:
        """ 컴퓨터 종료 메소드 """
        # 컴퓨터 끄기
        os.system('shutdown -s -t 3600')
        time.sleep(10.0)

        # 취소
        os.system('shutdown -a')

def run()-> None:
    # GUI Instance
    gui = GUI()

    gui.main()

if __name__ == '__main__':
    run()