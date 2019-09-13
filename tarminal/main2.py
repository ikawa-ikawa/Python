#/usr/bin/env python
#coding: utf-8
#from ファイルパス import 関数名


import sys
from tkinter import*


path = "~"
inp = []
InputBox = 0






def main():


    A()

        
        
def enter(event):
    
    global path
    
    inp.append( InputBox.get() )
    
    print("input = {}". format(inp))
    
    InputBox.delete( 0, END )
    
    
    label = Label( text = inp, fg = "#ffffff", bg = "#000000" )
    label.place( y = 0 )
    
    label_path = Label( text = path )
    label_path.place( x = 0, y = 0 )



def A():
    
    #メインウィンドウを立ち上げ
    root = Tk()
    root.title("タイトル")
    root.wm_attributes("-alpha", 0.5)
    root.configure(bg = "#000000" )
    root.geometry("600x300")




    #入力ボックス
    global InputBox
    InputBox = Entry(master = root, width = 20)
    #入力ボックスを配置
    InputBox.pack(side = "bottom")
    #入力ボックスをアクティブにする
    InputBox.focus_set()
    

    InputBox.bind("<Return>", enter)




    root.mainloop()





if __name__ == "__main__":
    main()







