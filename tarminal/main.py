#/usr/bin/env python
#coding: utf-8
#from ファイルパス import 関数名

import wx
import wx.lib.scrolledpanel as scrolled
import time
import threading
import subprocess
import os
import re




#入力したものを蓄積
inp = []

#どのターミナルがアクティブか
active_tarm = "yukari"

def dammy():
    pass

thread_yukari = threading.Thread(target = dammy)
thread_kaede = threading.Thread(target = dammy)
thread_kurumi = threading.Thread(target = dammy)

home = "/Users"
path_yukari = home
path_kaede = home
path_kurumi = home







class MyApp(wx.Frame):

    def __init__( self, *args, **kw ):
        
        super(MyApp, self).__init__(*args, **kw)
        self.init_ui()


    def init_ui(self):
        
        self.SetTitle("タイトル")
        self.SetBackgroundColour("#000000")
        self.SetPosition( (100, 100) )
        self.SetSize( (1000, 600) )
        
        self.Show()
        
        panel_tarm_1 = wx.Panel(self, -1, pos=(10, 10), size=(625, 400))
        panel_tarm_2 = wx.Panel(self, -1, pos=(645, 10), size =(625, 400))
        panel_tarm_3 = wx.Panel(self, -1, pos=(10, 420), size =(625, 400))
        panel_tarm_4 = wx.Panel(self, -1, pos=(645, 420), size =(625, 400))
        panel_tarm_1.SetBackgroundColour( (30, 30, 30) )
        panel_tarm_2.SetBackgroundColour( (30, 30, 30) )
        panel_tarm_3.SetBackgroundColour( (30, 30, 30) )
        panel_tarm_4.SetBackgroundColour( (30, 30, 30) )
        
        self.text_1 = wx.StaticText(panel_tarm_1, -1, 'ここにテキスト', pos=(10, 390))
        self.text_1.SetForegroundColour("#FFFFFF")
        
        #入力ボックス
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.TextBox = wx.TextCtrl(self, -1, size = (200, -1), pos=(10, 500), style = wx.TE_PROCESS_ENTER)
        self.TextBox.SetForegroundColour("#00FF00")
        self.TextBox.SetBackgroundColour("#000000")
        self.TextBox.SetFont(font)
        
        
        self.TextBox.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)


    def OnTextEnter(self, event):
        global inp
        global active_tarm
        global thread_yukari
        global thread_kaede
        global thread_kurumi
        
        
        inp.append( self.TextBox.GetValue() )
        self.TextBox.Clear()
        print("input = {}".format(inp))
        
        if inp[-1] == "active yukari":
            print("ゆかりターミナルをアクティブにしました")
            active_tarm = "yukari"
        
        if inp[-1] == "active kaede":
            print("かえでターミナルをアクティブにしました")
            active_tarm = "kaede"
        
        if inp[-1] == "active kurumi":
            print("くるみターミナルをアクティブにしました")
            active_tarm = "kurumi"
        
        if inp[-1] == "exit":
            if thread_yukari.is_alive() == False and thread_kaede.is_alive() == False and thread_kurumi.is_alive() == False:
                self.Close()
            else:
                print("スレッドが生きています")
 
        if active_tarm == "yukari":
            
            if thread_yukari.is_alive() == False:
                thread_yukari = threading.Thread(target = self.command, args=[active_tarm] )
                thread_yukari.start()
            else:
                print("yukari:スレッドが終了していません")


        if active_tarm == "kaede":

            if thread_kaede.is_alive() == False:
                thread_kaede = threading.Thread(target = self.command, args=[active_tarm])
                thread_kaede.start()
            else:
                print("kaede:スレッドが終了していません")


        if active_tarm == "kurumi":
    
            if thread_kurumi.is_alive() == False:
                thread_kurumi = threading.Thread(target = self.command, args=[active_tarm])
                thread_kurumi.start()
            else:
                print("kurumi:スレッドが終了していません")






    def command(self, tarm_name):
        
        global thread_yukari
        global thread_kaede
        global path_yukari
        global path_kaede
        global path_kurumi
        
        str = ""
        
        if len(inp) > 0:
            str = inp[-1]
        
        
        if str == "pwd":
            if tarm_name == "yukari": print("pwd:{}".format(path_yukari))
            if tarm_name == "kaede": print("pwd:{}".format(path_kaede))
            if tarm_name == "kurumi": print("pwd:{}".format(path_kurumi))
        
        
        
        if str.split()[0] == "ls":
            if tarm_name == "yukari": file = os.listdir(path_yukari)
            if tarm_name == "kaede": file = os.listdir(path_kaede)
            if tarm_name == "kurumi": file = os.listdir(path_kurumi)
            #隠しファイルも出力してしまうため先頭一文字が"."の場合リストから削除
            cnt = 0
            for x in file:
                if(x[0] == "."):
                    del file[cnt]
                cnt = cnt + 1
            
            for x in file:
                print(x)
        
        
        if str.split()[0] == "cd":
            
            global home
            
            
            #入力が"cd"の場合homeに戻る
            if len( str.split() ) <= 1:
                if tarm_name == "yukari": path_yukari = home
                if tarm_name == "kaede": path_kurumi = home
                if tarm_name == "kurumi": path_kaede = home
            
            else:
                match = 0
                #pathに存在するファイルを取得
                if tarm_name == "yukari": file = os.listdir(path_yukari)
                if tarm_name == "kaede": file = os.listdir(path_kaede)
                if tarm_name == "kurumi": file = os.listdir(path_kurumi)
                #取得した中にcdの第二引数と一致するファイルがあった場合pathに追記．
                for x in file:
                    if str.split()[1].upper() == x.upper() :
                        match = 1
                        if tarm_name == "yukari": path_yukari = path_yukari + "/" + x
                        if tarm_name == "kaede": path_kaede = path_kaede + "/" + x
                        if tarm_name == "kurumi": path_kurumi = path_kurumi + "/" + x
                #なかった場合かつ第二引数が".."の場合はディレクトリを戻る．　第二引数のファイルが見当たらない場合はエラー
                if match == 0:
                    if str.split()[1] == "..":
                        if tarm_name == "yukari": path_list = path_yukari.split("/")
                        if tarm_name == "kaede": path_list = path_kaede.split("/")
                        if tarm_name == "kurumi": path_list = path_kurumi.split("/")

                        #homeより前には戻らないようにする
                        if len(path_list) <= 2:
                            print("not go")
                        else:
                            del path_list[-1]
                            path_list2 = ""
                            for x in path_list:
                                path_list2 = path_list2 + x
                            if tarm_name == "yukari": path_yukari = "/" + path_list2
                            if tarm_name == "kaede": path_kaede = "/" + path_list2
                            if tarm_name == "kurumi": path_kurumi = "/" + path_list2
                    else:
                        print("Not found : {}". format(str.split()[1]) )

                match = 0



        if str == "sleep":
            print("{} : 15秒スリープします". format(tarm_name))
            time.sleep(15)
            print("{} : スリープを終了します". format(tarm_name))

        



def A():
    
    
    app = wx.App()

    MyApp(None)

    app.MainLoop()
    
    print("Aを終了します")




def main():


#thread1 = threading.Thread(target = B)

#thread1.start()



    A()

#thread1.join()
        
        







if __name__ == "__main__":
    main()


