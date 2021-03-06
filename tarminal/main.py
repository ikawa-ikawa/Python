#/usr/bin/env python
#coding: utf-8
#from ファイルパス import 関数名

import wx           #GUI
import time         #時間（タイマー）
import threading    #スレッド
import subprocess   #サブプロセス
import os           #OS
import re           #正規表現
import datetime     #時間（日時）
import shlex        #なんだっけこれ
import psutil       #CPU使用率とか

from subprocess import check_output




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

#フラグ
flag_exit = 0

per_mem = 0
per_cpu = 0


#画像
draw_cpu = 0
draw_mem = 0

path_anime_cnt_yukari = 0
path_anime_cnt_kaede = 0
path_anime_cnt_kurumi = 0





class MyApp(wx.Frame):

    def __init__( self, *args, **kw ):
        
        super(MyApp, self).__init__(*args, **kw)
        self.init_ui()


    def init_ui(self):
        
        global font
        global thread_cpu
        global c_cpu
        global c_mem
        global c_tarm
        global yukari_path
        global kaede_path
        global kurumi_path
        global yukari_path_null
        global kaede_path_null
        global kurumi_path_null
        
        global yukari_page_1
        global yukari_page_10
        global yukari_page_100
        global yukari_page_down_1
        global yukari_page_down_10
        global yukari_page_down_100
        global kaede_page_1
        global kaede_page_10
        global kaede_page_100
        global kaede_page_down_1
        global kaede_page_down_10
        global kaede_page_down_100
        global kurumi_page_1
        global kurumi_page_10
        global kurumi_page_100
        global kurumi_page_down_1
        global kurumi_page_down_10
        global kurumi_page_down_100

        
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        thread_cpu = threading.Thread(target = self.getcpu)
        
        self.SetTitle("タイトル")
        self.SetBackgroundColour("#000000")
        self.SetPosition( (100, 100) )
        self.SetSize( (1000, 600) )
        
        
        self.panel_tarm_1 = wx.Panel(self, -1, pos=(10, 10), size=(625, 400))
        self.panel_tarm_2 = wx.Panel(self, -1, pos=(645, 10), size =(625, 400))
        self.panel_tarm_3 = wx.Panel(self, -1, pos=(10, 420), size =(625, 400))
        self.panel_tarm_1.SetBackgroundColour( (30, 30, 30) )
        self.panel_tarm_2.SetBackgroundColour( (30, 30, 30) )
        self.panel_tarm_3.SetBackgroundColour( (30, 30, 30) )

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
        self.TextBox = wx.TextCtrl(self, -1, size = (630, -1), pos=(645, 765), style = wx.TE_PROCESS_ENTER)
        self.TextBox.SetForegroundColour("#00FF00")
        self.TextBox.SetBackgroundColour("#000000")
        self.TextBox.SetFont(font)
        
        self.TextBox.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
        self.TextBox.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        
        #画像
        image = wx.Image("img/circle_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = ( 645, 420 ), size = image.GetSize() )
        
        image = wx.Image("img/circle_tarm_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = ( 645, 420 ), size = image.GetSize() )
        
        image = wx.Image("img/circle_cpu_0.png")
        c_cpu = image.ConvertToBitmap()
        self.c_cpu = wx.StaticBitmap(self, -1, c_cpu, pos = ( 645, 420 ), size = image.GetSize() )
        
        image = wx.Image("img/circle_mem_0.png")
        c_mem = image.ConvertToBitmap()
        self.c_mem = wx.StaticBitmap(self, -1, c_mem, pos = ( 645, 420 ), size = image.GetSize() )
        
        image = wx.Image("img/circle_tarm_yukari.png")
        c_tarm = image.ConvertToBitmap()
        self.c_tarm = wx.StaticBitmap(self, -1, c_tarm, pos = ( 645, 420 ), size = image.GetSize() )
        
        
        image = wx.Image("img/path_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = ( 870, 420 ), size = image.GetSize() )
        
        image = wx.Image("img/path_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = ( 920, 454 ), size = image.GetSize() )

        image = wx.Image("img/path_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = ( 950, 490 ), size = image.GetSize() )
        
        
        #ページ番号
        image = wx.Image("img/page_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = (1030, 550), size = image.GetSize() )
        
        image = wx.Image("img/page_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = (1110, 550), size = image.GetSize() )
        
        image = wx.Image("img/page_base.png")
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap, pos = (1190, 550), size = image.GetSize() )
        
        
        image = wx.Image("img/number_0.png")
        yukari_page_100 = image.ConvertToBitmap()
        self.yukari_page_100 = wx.StaticBitmap(self, -1, yukari_page_100, pos = (1040, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        yukari_page_10 = image.ConvertToBitmap()
        self.yukari_page_10 = wx.StaticBitmap(self, -1, yukari_page_10, pos = (1055, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_1.png")
        yukari_page_1 = image.ConvertToBitmap()
        self.yukari_page_1 = wx.StaticBitmap(self, -1, yukari_page_1, pos = (1070, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        yukari_page_down_100 = image.ConvertToBitmap()
        self.yukari_page_down_100 = wx.StaticBitmap(self, -1, yukari_page_down_100, pos = (1040, 605), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        yukari_page_down_10 = image.ConvertToBitmap()
        self.yukari_page_down_10 = wx.StaticBitmap(self, -1, yukari_page_down_10, pos = (1055, 605), size = image.GetSize() )
        
        image = wx.Image("img/number_1.png")
        yukari_page_down_1 = image.ConvertToBitmap()
        self.yukari_page_down_1 = wx.StaticBitmap(self, -1, yukari_page_down_1, pos = (1070, 605), size = image.GetSize() )
        
        
        image = wx.Image("img/number_0.png")
        kaede_page_100 = image.ConvertToBitmap()
        self.kaede_page_100 = wx.StaticBitmap(self, -1, kaede_page_100, pos = (1120, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        kaede_page_10 = image.ConvertToBitmap()
        self.kaede_page_10 = wx.StaticBitmap(self, -1, kaede_page_10, pos = (1135, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_1.png")
        kaede_page_1 = image.ConvertToBitmap()
        self.kaede_page_1 = wx.StaticBitmap(self, -1, kaede_page_1, pos = (1150, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        kaede_page_down_100 = image.ConvertToBitmap()
        self.kaede_page_down_100 = wx.StaticBitmap(self, -1, kaede_page_down_100, pos = (1120, 605), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        kaede_page_down_10 = image.ConvertToBitmap()
        self.kaede_page_down_10 = wx.StaticBitmap(self, -1, kaede_page_down_10, pos = (1135, 605), size = image.GetSize() )
        
        image = wx.Image("img/number_1.png")
        kaede_page_down_1 = image.ConvertToBitmap()
        self.kaede_page_down_1 = wx.StaticBitmap(self, -1, kaede_page_down_1, pos = (1150, 605), size = image.GetSize() )
        
        
        image = wx.Image("img/number_0.png")
        kurumi_page_100 = image.ConvertToBitmap()
        self.kurumi_page_100 = wx.StaticBitmap(self, -1, kurumi_page_100, pos = (1200, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        kurumi_page_10 = image.ConvertToBitmap()
        self.kurumi_page_10 = wx.StaticBitmap(self, -1, kurumi_page_10, pos = (1215, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_1.png")
        kurumi_page_1 = image.ConvertToBitmap()
        self.kurumi_page_1 = wx.StaticBitmap(self, -1, kurumi_page_1, pos = (1230, 575), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        kurumi_page_down_100 = image.ConvertToBitmap()
        self.kurumi_page_down_100 = wx.StaticBitmap(self, -1, kurumi_page_down_100, pos = (1200, 605), size = image.GetSize() )
        
        image = wx.Image("img/number_0.png")
        kurumi_page_down_10 = image.ConvertToBitmap()
        self.kurumi_page_down_10 = wx.StaticBitmap(self, -1, kurumi_page_down_10, pos = (1215, 605), size = image.GetSize() )
        
        image = wx.Image("img/number_1.png")
        kurumi_page_down_1 = image.ConvertToBitmap()
        self.kurumi_page_down_1 = wx.StaticBitmap(self, -1, kurumi_page_down_1, pos = (1230, 605), size = image.GetSize() )
        
        
    
        
        
        #パス
        image = wx.Image("img/path_null.png")
        yukari_path_null = image.ConvertToBitmap()
        self.yukari_path_null = wx.StaticBitmap(self, -1, yukari_path_null, pos = ( 870, 420 ), size = image.GetSize() )
        
        image = wx.Image("img/path_null.png")
        kaede_path_null = image.ConvertToBitmap()
        self.kaede_path_null = wx.StaticBitmap(self, -1, kaede_path_null, pos = ( 920, 454 ), size = image.GetSize() )
        
        image = wx.Image("img/path_null.png")
        kurumi_path_null = image.ConvertToBitmap()
        self.kurumi_path_null = wx.StaticBitmap(self, -1, kurumi_path_null, pos = ( 950, 490 ), size = image.GetSize() )
        
        

        image = wx.Image("img/path_0.png")
        yukari_path = image.ConvertToBitmap()
        self.yukari_path = wx.StaticBitmap(self, -1, yukari_path, pos = ( 870, 420 ), size = image.GetSize() )

        image = wx.Image("img/path_0.png")
        kaede_path = image.ConvertToBitmap()
        self.kaede_path = wx.StaticBitmap(self, -1, kaede_path, pos = ( 920, 454 ), size = image.GetSize() )
        
        image = wx.Image("img/path_0.png")
        kurumi_path = image.ConvertToBitmap()
        self.kurumi_path = wx.StaticBitmap(self, -1, kurumi_path, pos = ( 950, 490 ), size = image.GetSize() )


        #パスを常に表示
        self.text_yukari_path = wx.StaticText(self, -1, path_yukari, pos=(1005, 425))
        self.text_yukari_path.SetFont(font)
        self.text_yukari_path.SetForegroundColour("#00FF00")
        
        self.text_kaede_path = wx.StaticText(self, -1, path_kaede, pos=(1055, 459))
        self.text_kaede_path.SetFont(font)
        self.text_kaede_path.SetForegroundColour("#00FF00")
        
        self.text_kurumi_path = wx.StaticText(self, -1, path_kurumi, pos=(1085, 495))
        self.text_kurumi_path.SetFont(font)
        self.text_kurumi_path.SetForegroundColour("#00FF00")

        #タイマー
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.anime)
        self.timer.Start(100)
        

        #閉じるボタンを押した時の処理( self.CLoseが呼ばれた時も呼ばれるらしい )
        self.Bind(wx.EVT_CLOSE, self.frame_close)
    
        #スレッド(CPU使用率取得)
        thread_cpu.start()
    

    
    #　閉じるボタンを押した時の処理
    def frame_close( self, event ):
        global flag_exit
        global thread_yukari
        global thread_kaede
        global thread_kurumi

        if thread_yukari.is_alive() == False and thread_kaede.is_alive() == False and thread_kurumi.is_alive() == False:
            flag_exit = 1
            thread_cpu.join()
            print("-----CPUスレッドが正常に終了しました-----")
            wx.Exit()
        else:
            print("スレッドが生きています")

    
    #　CPU使用率を取得
    def getcpu(self):
        global per_mem
        global per_cpu
        
        while flag_exit == 0:
            #CPU使用率
            per_mem = psutil.virtual_memory()
            per_mem = per_mem.percent
            per_cpu = psutil.cpu_percent(interval=1)
            time.sleep(0.1)

    #　常に更新
    def anime(self, event):
        global font
        
        global active_tarm
        
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
        
        global draw_page_yukari
        global draw_page_kaede
        global draw_page_kurumi
        
        global maxindex_yukari
        global maxindex_kaede
        global maxindex_kurumi
        
        global per_mem
        global per_cpu
        
        global draw_cpu
        global draw_mem
        
        global c_cpu
        global c_mem
        global c_tarm
        
        global yukari_path
        global kaede_path
        global kurumi_path
        global yukari_path_null
        global kaede_path_null
        global kurumi_path_null
        
        global path_anime_cnt_yukari
        global path_anime_cnt_kaede
        global path_anime_cnt_kurumi
        
        #ページ番号
        global yukari_page_1
        global yukari_page_10
        global yukari_page_100
        global yukari_page_down_1
        global yukari_page_down_10
        global yukari_page_down_100
        global kaede_page_1
        global kaede_page_10
        global kaede_page_100
        global kaede_page_down_1
        global kaede_page_down_10
        global kaede_page_down_100
        global kurumi_page_1
        global kurumi_page_10
        global kurumi_page_100
        global kurumi_page_down_1
        global kurumi_page_down_10
        global kurumi_page_down_100
        
        #ページ番号(分母)
        global page_yukari
        global page_kaede
        global page_kurumi

        #ページ番号(分子)
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
        
        #パスアニメのカウントアップ
        if active_tarm == "yukari" :  path_anime_cnt_yukari = path_anime_cnt_yukari + 1
        if active_tarm == "kaede" :  path_anime_cnt_kaede = path_anime_cnt_kaede + 1
        if active_tarm == "kurumi" :  path_anime_cnt_kurumi = path_anime_cnt_kurumi + 1
        
        if path_anime_cnt_yukari >= 10 or path_anime_cnt_kaede >= 10 or path_anime_cnt_kurumi >= 10:
            path_anime_cnt_yukari = 0
            path_anime_cnt_kaede = 0
            path_anime_cnt_kurumi = 0
        

        #画像系
        n_cpu = int((per_cpu - int(per_cpu)) * 10)
        n_mem = int((per_mem - int(per_mem)) * 10)
        
        if n_cpu == draw_cpu:
            pass
        elif n_cpu > draw_cpu:
            draw_cpu = draw_cpu + 1
        else:
            draw_cpu = draw_cpu - 1
        
        if n_mem == draw_mem:
            pass
        elif n_mem > draw_mem:
            draw_mem = draw_mem + 1
        else:
            draw_mem = draw_mem - 1

        #CPU，MEMアニメ
        self.c_cpu.SetBitmap(wx.Bitmap("img/circle_cpu_" + str(draw_cpu) + ".png"))
        self.c_mem.SetBitmap(wx.Bitmap("img/circle_mem_" + str(draw_mem) + ".png"))
        
        #アクティブターミナル
        if active_tarm == "yukari" : self.c_tarm.SetBitmap(wx.Bitmap("img/circle_tarm_yukari.png"))
        if active_tarm == "kaede" : self.c_tarm.SetBitmap(wx.Bitmap("img/circle_tarm_kaede.png"))
        if active_tarm == "kurumi" : self.c_tarm.SetBitmap(wx.Bitmap("img/circle_tarm_kurumi.png"))

        #パスアニメ
        self.yukari_path.SetBitmap(wx.Bitmap("img/path_" + str(path_anime_cnt_yukari) + ".png"))
        self.kaede_path.SetBitmap(wx.Bitmap("img/path_" + str(path_anime_cnt_kaede) + ".png"))
        self.kurumi_path.SetBitmap(wx.Bitmap("img/path_" + str(path_anime_cnt_kurumi) + ".png"))
        
        #ページ番号
        self.yukari_page_100.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_yukari / 100)) + ".png"))
        self.yukari_page_10.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_yukari / 10)) + ".png"))
        self.yukari_page_1.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_yukari / 1)) + ".png"))
        self.yukari_page_down_100.SetBitmap(wx.Bitmap("img/number_" + str(int(page_yukari / 100)) + ".png"))
        self.yukari_page_down_10.SetBitmap(wx.Bitmap("img/number_" + str(int(page_yukari / 10)) + ".png"))
        self.yukari_page_down_1.SetBitmap(wx.Bitmap("img/number_" + str(int(page_yukari / 1)) + ".png"))
        
        self.kaede_page_100.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_kaede / 100)) + ".png"))
        self.kaede_page_10.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_kaede / 10)) + ".png"))
        self.kaede_page_1.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_kaede / 1)) + ".png"))
        self.kaede_page_down_100.SetBitmap(wx.Bitmap("img/number_" + str(int(page_kaede / 100)) + ".png"))
        self.kaede_page_down_10.SetBitmap(wx.Bitmap("img/number_" + str(int(page_kaede / 10)) + ".png"))
        self.kaede_page_down_1.SetBitmap(wx.Bitmap("img/number_" + str(int(page_kaede / 1)) + ".png"))
        
        self.kurumi_page_100.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_kurumi / 100)) + ".png"))
        self.kurumi_page_10.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_kurumi / 10)) + ".png"))
        self.kurumi_page_1.SetBitmap(wx.Bitmap("img/number_" + str(int(draw_page_kurumi / 1)) + ".png"))
        self.kurumi_page_down_100.SetBitmap(wx.Bitmap("img/number_" + str(int(page_kurumi / 100)) + ".png"))
        self.kurumi_page_down_10.SetBitmap(wx.Bitmap("img/number_" + str(int(page_kurumi / 10)) + ".png"))
        self.kurumi_page_down_1.SetBitmap(wx.Bitmap("img/number_" + str(int(page_kurumi / 1)) + ".png"))



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
        global flag_exit
        global path_anime_cnt_yukari
        global path_anime_cnt_kaede
        global path_anime_cnt_kurumi

        

        #インプットリストに追加
        inp.append( self.TextBox.GetValue() )
        if active_tarm == "yukari": inp_yukari.append( self.TextBox.GetValue() )
        if active_tarm == "kaede": inp_kaede.append( self.TextBox.GetValue() )
        if active_tarm == "kurumi": inp_kurumi.append( self.TextBox.GetValue() )
        

        #テキストボックスの内容を削除
        self.TextBox.Clear()
        
        self.printbar(active_tarm)
        
        
        #アクティブコマンド
        if inp[-1] == "active yukari" or inp[-1] == "on yukari" or inp[-1] == "active 1" or inp[-1] == "on 1":
            active_tarm = "yukari"
            self.printf(active_tarm, "Activate Yukari")
            path_anime_cnt_yukari = 0
            path_anime_cnt_kaede = 0
            path_anime_cnt_kurumi = 0
        
        if inp[-1] == "active kaede" or inp[-1] == "on kaede" or inp[-1] == "active 2" or inp[-1] == "on 2":
            active_tarm = "kaede"
            self.printf(active_tarm, "Activate Kaede")
            path_anime_cnt_yukari = 0
            path_anime_cnt_kaede = 0
            path_anime_cnt_kurumi = 0
        
        if inp[-1] == "active kurumi" or inp[-1] == "on kurumi" or inp[-1] == "active 3" or inp[-1] == "on 3":
            active_tarm = "kurumi"
            self.printf(active_tarm, "Activate Kurumi")
            path_anime_cnt_yukari = 0
            path_anime_cnt_kaede = 0
            path_anime_cnt_kurumi = 0
        
        #exitコマンド
        if inp[-1] == "exit":
            self.frame_close(self)


 
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
        
        # pwd
        if str1 == "pwd":
            if tarm_name == "yukari": self.printf(tarm_name, path_yukari )
            if tarm_name == "kaede": self.printf(tarm_name, path_kaede )
            if tarm_name == "kurumi": self.printf(tarm_name, path_kurumi )
        
        # back bc bk
        elif str1 == "back" or str1 == "bc" or str1 == "bk":
            if tarm_name == "yukari" and page_yukari >= draw_page_yukari and draw_page_yukari != 1: draw_page_yukari = draw_page_yukari - 1
            if tarm_name == "kaede" and page_kaede >= draw_page_kaede and draw_page_kaede != 1: draw_page_kaede = draw_page_kaede - 1
            if tarm_name == "kurumi" and page_kurumi >= draw_page_kurumi and draw_page_kurumi != 1: draw_page_kurumi = draw_page_kurumi - 1

        # go
        elif str1 == "go":
            if tarm_name == "yukari" and page_yukari > draw_page_yukari: draw_page_yukari = draw_page_yukari + 1
            if tarm_name == "kaede" and page_kaede > draw_page_kaede: draw_page_kaede = draw_page_kaede + 1
            if tarm_name == "kurumi" and page_kurumi > draw_page_kurumi: draw_page_kurumi = draw_page_kurumi + 1

        # end
        elif str1 == "end":
            if tarm_name == "yukari" and page_yukari > draw_page_yukari: draw_page_yukari = page_yukari
            if tarm_name == "kaede" and page_kaede > draw_page_kaede: draw_page_kaede = page_kaede
            if tarm_name == "kurumi" and page_kurumi > draw_page_kurumi: draw_page_kurumi = page_kurumi
        
        # python
        elif  str1.split(" ")[0] == "python":
            if len(str1.rstrip(" ").split(" ")) >= 2:
                if tarm_name == "yukari" : p = path_yukari + "/" + str1.split()[1]
                if tarm_name == "kaede" : p = path_kaede + "/" + str1.split()[1]
                if tarm_name == "kurumi" : p = path_kurumi + "/" + str1.split()[1]
                proc = subprocess.Popen(["python", p], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                std, err = proc.communicate()
                std = std.decode("utf-8")
                err = err.decode("utf-8")
                if len(std) != 0 :
                    for line in std.rstrip("\n").split("\n"):
                        self.printf(tarm_name, line)
                if len(err) != 0 :
                    for line in err.rstrip("\n").split("\n"):
                        self.printf(tarm_name, line)
        
        # open
        elif str1.split(" ")[0] == "open":
            if len(str1.rstrip(" ").split(" ")) >= 2:
                if tarm_name == "yukari" : p = path_yukari + "/" + str1.split()[1]
                if tarm_name == "kaede" : p = path_kaede + "/" + str1.split()[1]
                if tarm_name == "kurumi" : p = path_kurumi + "/" + str1.split()[1]
                proc = subprocess.Popen(["open", p], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                std, err = proc.communicate()
                std = std.decode("utf-8")
                err = err.decode("utf-8")
                if len(std) != 0 :
                    for line in std.rstrip("\n").split("\n"):
                        self.printf(tarm_name, line)
                if len(err) != 0 :
                    for line in err.rstrip("\n").split("\n"):
                        self.printf(tarm_name, line)


        # clear
        elif str1 == "clear":
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

        # allclear
        elif str1 == "allclear":
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

        # sleep
        elif str1 == "sleep":
            self.printf(tarm_name, "スリープを実行")
            time.sleep(15)
            self.printf(tarm_name, "スリープを終了")

        # ls
        elif str1.split(" ")[0] == "ls":
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
        
        # cd
        elif str1.split(" ")[0] == "cd":
            
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
                    if str1.split(" ")[1] == "..":
                        path_list = ""
                        if tarm_name == "yukari": path_list = path_yukari.split("/")
                        if tarm_name == "kaede": path_list = path_kaede.split("/")
                        if tarm_name == "kurumi": path_list = path_kurumi.split("/")

                        #homeより前には戻らないようにする
                        if len(path_list) <= 2:
                            self.printf(tarm_name , "can not change directory")
                        else:
                            del path_list[-1]
                            del path_list[0]
                            path_list2 = ""
                            for x in path_list:
                                path_list2 = path_list2 + "/" + x
                            if tarm_name == "yukari": path_yukari = path_list2
                            if tarm_name == "kaede": path_kaede = path_list2
                            if tarm_name == "kurumi": path_kurumi = path_list2
                    else:
                        self.printf(tarm_name, "No such file or directory : " + str( str1.split()[1] ))

                match = 0
        
                    
        elif len(str1.split(" ")) > 0 :
            #アクティブ化のコマンドに間違いがある場合エラーメッセージを表示
            if (str1.split(" ")[0] == "active" or str1.split(" ")[0] == "on") and len(str1.split(" ") ) <= 1:
                self.printf(tarm_name, "No second argument - yukari or kaede or kurumi or 1 or 2 or 3")
            elif (str1.split(" ")[0] == "active" or str1.split(" ")[0] == "on") :
                if str1 != "active yukari" and str1 != "active kaede" and str1 != "active kurumi" and str1 != "on yukari" and str1 != "on kaede" and str1 != "on kurumi" and str1 != "active 1" and str1 != "active 2" and str1 != "active 3" and str1 != "on 1" and str1 != "on 2" and str1 != "on 3":
                    self.printf(tarm_name, "The second argument is wrong - yukari or kaede or kurumi or 1 or 2 or 3")
            #その他未知コマンドが入力された場合はsubprosessに投げる
            else :
                cmd = shlex.split(str1)
                proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                std, err = proc.communicate()
                std = std.decode("utf-8")
                err = err.decode("utf-8")
                if len(std) != 0 :
                    for line in std.rstrip("\n").split("\n"):
                        self.printf(tarm_name, line)
                if len(err) != 0 :
                    for line in err.rstrip("\n").split("\n"):
                        self.printf(tarm_name, line)



        #パスの中身を表示
        self.text_yukari_path.SetLabel(path_yukari)
        self.text_kaede_path.SetLabel(path_kaede)
        self.text_kurumi_path.SetLabel(path_kurumi)


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
    
    print("-----メインスレッドが正常に終了しました-----")




def main():


    A()



if __name__ == "__main__":
    main()








