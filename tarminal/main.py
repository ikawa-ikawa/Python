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
import datetime




#入力したものを蓄積
inp = []
inp_yukari = []
inp_kaede = []
inp_kurumi = []

#画面に表示すべき文字列を格納
out_yukari = []
out_kaede = []
out_kurumi = []

#画面に表示できる最大の要素数
maxindex_yukari = 22
maxindex_kaede = 22
maxindex_kurumi = 22

#ページ番号
page_yukari = 1
page_kaede = 1
page_kurumi = 1

draw_page_yukari = 1
draw_page_kaede = 1
draw_page_kurumi = 1

#上下キーが押された時に必要
pointer_yukari = 0
pointer_kaede = 0
pointer_kurumi = 0

#文字表示の場所
y_yukari = 0
y_kaede = 0
y_kurumi = 0
x_yukari = 10
x_kaede = 10
x_kurumi = 10

#パス
home = "/Users"
path_yukari = home
path_kaede = home
path_kurumi = home

#どのターミナルがアクティブか
active_tarm = "yukari"

def dammy():
    pass

thread_yukari = threading.Thread(target = dammy)
thread_kaede = threading.Thread(target = dammy)
thread_kurumi = threading.Thread(target = dammy)









class MyApp(wx.Frame):

    def __init__( self, *args, **kw ):
        
        super(MyApp, self).__init__(*args, **kw)
        self.init_ui()


    def init_ui(self):
        
        global font
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        self.SetTitle("タイトル")
        self.SetBackgroundColour("#000000")
        self.SetPosition( (100, 100) )
        self.SetSize( (1000, 600) )
        
        
        self.panel_tarm_1 = wx.Panel(self, -1, pos=(10, 10), size=(625, 400))
        self.panel_tarm_2 = wx.Panel(self, -1, pos=(645, 10), size =(625, 400))
        self.panel_tarm_3 = wx.Panel(self, -1, pos=(10, 420), size =(625, 400))
        self.panel_tarm_4 = wx.Panel(self, -1, pos=(645, 420), size =(625, 400))
        self.panel_tarm_1.SetBackgroundColour( (30, 30, 30) )
        self.panel_tarm_2.SetBackgroundColour( (30, 30, 30) )
        self.panel_tarm_3.SetBackgroundColour( (30, 30, 30) )
        self.panel_tarm_4.SetBackgroundColour( (30, 30, 30) )

        self.text_1 = wx.StaticText(self.panel_tarm_1, -1, "", pos=(x_yukari, y_yukari))
        self.text_1.SetFont(font)
        self.text_1.SetForegroundColour("#00FF00")
        self.text_2 = wx.StaticText(self.panel_tarm_2, -1, "", pos=(x_kaede, y_kaede))
        self.text_2.SetFont(font)
        self.text_2.SetForegroundColour("#00FF00")
        self.text_3 = wx.StaticText(self.panel_tarm_3, -1, "", pos=(x_kurumi, y_kurumi))
        self.text_3.SetFont(font)
        self.text_3.SetForegroundColour("#00FF00")
        
        self.Show(True)
       
    
        #入力ボックス
        self.TextBox = wx.TextCtrl(self, -1, size = (200, -1), pos=(645, 420), style = wx.TE_PROCESS_ENTER)
        self.TextBox.SetForegroundColour("#00FF00")
        self.TextBox.SetBackgroundColour("#000000")
        self.TextBox.SetFont(font)
        
        self.TextBox.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
        self.TextBox.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        
        
        #タイマー
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.anime)
        self.timer.Start(100)
    

    #　常に更新
    def anime(self, event):
        global font
        global y_yukari
        global y_kurumi
        global y_kaede
        global x_yukari
        global x_kurumi
        global x_kaede
        global out_yukari
        global out_kaede
        global out_kurumi
        global page_yukari
        global page_kaede
        global page_kurumi
        global maxindex_yukari
        global maxindex_kaede
        global maxindex_kurumi
        global draw_page_yukari
        global draw_page_kaede
        global draw_page_kurumi
        

        #ターミナル文字表示
        output_yukari = ""
        output_kaede = ""
        output_kurumi = ""

        #スライスで表示すべき文字列を取得
        for x in out_yukari[ draw_page_yukari * maxindex_yukari - maxindex_yukari : draw_page_yukari * maxindex_yukari ]:
            output_yukari = output_yukari + "\n" + x
        for x in out_kaede[ draw_page_kaede * maxindex_kaede - maxindex_kaede : draw_page_kaede * maxindex_kaede ]:
            output_kaede = output_kaede + "\n" + x
        for x in out_kurumi[ draw_page_kurumi * maxindex_kurumi - maxindex_kurumi : draw_page_kurumi * maxindex_kurumi ]:
            output_kurumi = output_kurumi + "\n" + x
    

        self.text_1.SetLabel(output_yukari)
        self.text_2.SetLabel(output_kaede)
        self.text_3.SetLabel(output_kurumi)
    
    
    #上下キーが押された時の処理
    def onKey(self, event):
    
        global pointer_yukari
        global pointer_kaede
        global pointer_kurumi
        global inp_yukari
        global inp_kaede
        global inp_kurumi
        
        if event.GetKeyCode() == wx.WXK_DOWN:
            if active_tarm == "yukari" and pointer_yukari < len(inp_yukari) - 1 :
                self.TextBox.Clear()
                pointer_yukari = pointer_yukari + 1
                self.TextBox.write( inp_yukari[ pointer_yukari ] )
            if active_tarm == "kaede" and pointer_kaede < len(inp_kaede) - 1 :
                self.TextBox.Clear()
                pointer_kaede = pointer_kaede + 1
                self.TextBox.write( inp_kaede[ pointer_kaede ] )
            if active_tarm == "kurumi" and pointer_kurumi < len(inp_kurumi) - 1 :
                self.TextBox.Clear()
                pointer_kurumi = pointer_kurumi + 1
                self.TextBox.write( inp_kurumi[ pointer_kurumi ] )
        elif event.GetKeyCode() == wx.WXK_UP:
            if active_tarm == "yukari" and pointer_yukari > 0 :
                self.TextBox.Clear()
                self.TextBox.write( inp_yukari[ pointer_yukari ] )
                pointer_yukari = pointer_yukari - 1
            if active_tarm == "kaede" and pointer_kaede > 0 :
                self.TextBox.Clear()
                self.TextBox.write( inp_kaede[ pointer_kaede ] )
                pointer_kaede = pointer_kaede - 1
            if active_tarm == "kurumi" and pointer_kurumi > 0 :
                self.TextBox.Clear()
                self.TextBox.write( inp_kurumi[ pointer_kurumi ] )
                pointer_kurumi = pointer_kurumi - 1
        
        else:
            event.Skip()

    #エンターキーが押された時の処理
    def OnTextEnter(self, event):
        global inp
        global pointer_yukari
        global pointer_kaede
        global pointer_kurumi
        global active_tarm
        global thread_yukari
        global thread_kaede
        global thread_kurumi
        global draw_page_yukari
        global draw_page_kaede
        global draw_page_kurumi
        global page_yukari
        global page_kaede
        global page_kurumi

        #インプットリストに追加
        inp.append( self.TextBox.GetValue() )
        if active_tarm == "yukari": inp_yukari.append( self.TextBox.GetValue() )
        if active_tarm == "kaede": inp_kaede.append( self.TextBox.GetValue() )
        if active_tarm == "kurumi": inp_kurumi.append( self.TextBox.GetValue() )
        

        #テキストボックスの内容を削除
        self.TextBox.Clear()
        print("input = {}".format(inp))
        
        self.printbar(active_tarm)
        
        #アクティブコマンド
        if inp[-1] == "active yukari" or inp[-1] == "on yukari" or inp[-1] == "active 1" or inp[-1] == "on 1":
            active_tarm = "yukari"
            self.printf(active_tarm, "Activate Yukari")
        
        if inp[-1] == "active kaede" or inp[-1] == "on kaede" or inp[-1] == "active 2" or inp[-1] == "on 2":
            active_tarm = "kaede"
            self.printf(active_tarm, "Activate Kaede")
        
        if inp[-1] == "active kurumi" or inp[-1] == "on kurumi" or inp[-1] == "active 3" or inp[-1] == "on 3":
            active_tarm = "kurumi"
            self.printf(active_tarm, "Activate Kurumi")
        
        if inp[-1] == "exit":
            if thread_yukari.is_alive() == False and thread_kaede.is_alive() == False and thread_kurumi.is_alive() == False:
                self.Close()
            else:
                print("スレッドが生きています")
 
 
        #スレッド処理
        if active_tarm == "yukari":
            
            pointer_yukari = len(inp_yukari) - 1
            
            if thread_yukari.is_alive() == False:
                thread_yukari = threading.Thread(target = self.command, args=[active_tarm] )
                thread_yukari.start()
            else:
                self.printf("yukari", "running thread")



        if active_tarm == "kaede":
            
            pointer_kaede = len(inp_kaede) - 1

            if thread_kaede.is_alive() == False:
                thread_kaede = threading.Thread(target = self.command, args=[active_tarm])
                thread_kaede.start()
            else:
                self.printf("kaede", "running thread")


        if active_tarm == "kurumi":
            
            pointer_kurumi = len(inp_kurumi) - 1
    
            if thread_kurumi.is_alive() == False:
                thread_kurumi = threading.Thread(target = self.command, args=[active_tarm])
                thread_kurumi.start()
            else:
                self.printf("kurumi", "running thread")
                    
                    





    def command(self, tarm_name):
        
        global inp
        global thread_yukari
        global thread_kaede
        global path_yukari
        global path_kaede
        global path_kurumi
        global draw_page_yukari
        global draw_page_kaede
        global draw_page_kurumi
        global page_yukari
        global page_kaede
        global page_kurumi
        global pointer_yukari
        global pointer_kaede
        global pointer_kurumi
        

        
        str1 = ""
        
        if len(inp) > 0:
            str1 = inp[-1]
        
        
        if str1 == "pwd":
            if tarm_name == "yukari": self.printf(tarm_name, path_yukari )
            if tarm_name == "kaede": self.printf(tarm_name, path_kaede )
            if tarm_name == "kurumi": self.printf(tarm_name, path_kurumi )
        
        if str1 == "back" or str1 == "bc" or str1 == "bk":
            if tarm_name == "yukari" and page_yukari >= draw_page_yukari and draw_page_yukari != 1: draw_page_yukari = draw_page_yukari - 1
            if tarm_name == "kaede" and page_kaede >= draw_page_kaede and draw_page_kaede != 1: draw_page_kaede = draw_page_kaede - 1
            if tarm_name == "kurumi" and page_kurumi >= draw_page_kurumi and draw_page_kurumi != 1: draw_page_kurumi = draw_page_kurumi - 1

        if str1 == "go":
            if tarm_name == "yukari" and page_yukari > draw_page_yukari: draw_page_yukari = draw_page_yukari + 1
            if tarm_name == "kaede" and page_kaede > draw_page_kaede: draw_page_kaede = draw_page_kaede + 1
            if tarm_name == "kurumi" and page_kurumi > draw_page_kurumi: draw_page_kurumi = draw_page_kurumi + 1

        if str1 == "end":
            if tarm_name == "yukari" and page_yukari > draw_page_yukari: draw_page_yukari = page_yukari
            if tarm_name == "kaede" and page_kaede > draw_page_kaede: draw_page_kaede = page_kaede
            if tarm_name == "kurumi" and page_kurumi > draw_page_kurumi: draw_page_kurumi = page_kurumi

        if str1 == "clear":
            if tarm_name == "yukari":
                inp_yukari.clear()
                out_yukari.clear()
                page_yukari = 1
                draw_page_yukari = page_yukari
                pointer_yukari = 0
            if tarm_name == "kaede":
                inp_kaede.clear()
                out_kaede.clear()
                page_kaede = 1
                draw_page_kaede = page_kaede
                pointer_kaede = 0
            if tarm_name == "kurumi":
                inp_kurumi.clear()
                out_kurumi.clear()
                page_kurumi = 1
                draw_page_kurumi = page_kurumi
                pointer_kurumi = 0

        if str1 == "allclear":
            inp_yukari.clear()
            inp_kaede.clear()
            inp_kurumi.clear()
            inp.clear()
            out_yukari.clear()
            out_kaede.clear()
            out_kurumi.clear()
            page_yukari = 1
            page_kaede = 1
            page_kurumi = 1
            draw_page_yukari = page_yukari
            draw_page_kaede = page_kaede
            draw_page_kurumi = page_kurumi
            pointer_yukari = 0
            pointer_kaede = 0
            pointer_kurumi = 0

        
        if str1 == "sleep":
            self.printf(tarm_name, "スリープを実行")
            time.sleep(15)
            self.printf(tarm_name, "スリープを終了")
        
        
        #エラー回避
        if str1 != "" :
        
        
        
            if str1.split()[0] == "ls":
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
                    self.printf(tarm_name, x)
            
            
            if str1.split()[0] == "cd":
                
                global home
                
                
                #入力が"cd"の場合homeに戻る
                if len( str1.split() ) <= 1:
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
                        if str1.split()[1].upper() == x.upper() :
                            match = 1
                            if tarm_name == "yukari": path_yukari = path_yukari + "/" + x
                            if tarm_name == "kaede": path_kaede = path_kaede + "/" + x
                            if tarm_name == "kurumi": path_kurumi = path_kurumi + "/" + x
                    #なかった場合かつ第二引数が".."の場合はディレクトリを戻る．　第二引数のファイルが見当たらない場合はエラー
                    if match == 0:
                        if str1.split()[1] == "..":
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
                            self.printf(tarm_name, "No such file or directory : " + str( str1.split()[1] ))

                    match = 0





        
    def printf(self, tarm_name, x):
        global y_yukari
        global y_kurumi
        global y_kaede
        global x_yukari
        global x_kurumi
        global x_kaede
        global out_yukari
        global out_kaede
        global out_kurumi
        global page_yukari
        global page_kaede
        global page_kurumi
        global maxindex_yukari
        global maxindex_kaede
        global maxindex_kurumi
        global draw_page_yukari
        global draw_page_kaede
        global draw_page_kurumi
        
        if tarm_name == "yukari":
            out_yukari.append(x)
            #ページ更新
            if len(out_yukari) > (page_yukari * maxindex_yukari) :
                page_yukari = page_yukari + 1
                draw_page_yukari = draw_page_yukari + 1
        if tarm_name == "kaede":
            out_kaede.append(x)
            #ページ更新
            if len(out_kaede) > (page_kaede * maxindex_kaede) :
                page_kaede = page_kaede + 1
                draw_page_kaede = draw_page_kaede + 1
        if tarm_name == "kurumi":
            out_kurumi.append(x)
            #ページ更新
            if len(out_kurumi) > (page_kurumi * maxindex_kurumi) :
                page_kurumi = page_kurumi + 1
                draw_page_kurumi = draw_page_kurumi + 1





    def printbar(self, tarm_name):
        global y_yukari
        global y_kurumi
        global y_kaede
        global x_yukari
        global x_kurumi
        global x_kaede
        global inp_yukari
        global inp_kaede
        global inp_kurumi
        global page_yukari
        global page_kaede
        global page_kurumi
        
        time = datetime.datetime.now()
        hour = time.hour
        minute = time.minute
        second = time.second
        
        cmd = ""
        page = ""
        
        if tarm_name == "yukari" and len(inp_yukari) > 0:
            cmd = inp_yukari[-1]
            page = page_yukari
        if tarm_name == "kaede" and len(inp_kaede) > 0:
            cmd = inp_kaede[-1]
            page = page_kaede
        if tarm_name == "kurumi" and len(inp_kaede) > 0:
            cmd = inp_kurumi[-1]
            page = page_kurumi
        
        txt = "-- " + tarm_name + " " + str(page) + " " + str(hour) + ":" + str(minute) + ":" + str(second) + " " + cmd + " --"
        
        if tarm_name == "yukari":
            out_yukari.append(txt)
        if tarm_name == "kaede":
            out_kaede.append(txt)
        if tarm_name == "kurumi":
            out_kurumi.append(txt)



def A():
    
    
    app = wx.App()

    MyApp(None)

    app.MainLoop()
    
    print("Aを終了します")




def main():


    A()



if __name__ == "__main__":
    main()








