#/usr/bin/env python
#coding: utf-8
#from ファイルパス import 関数名

import glob         #フォルダ探索
import csv          #scvファイル関係


#フォルダの探索を行い，そのファイルパスをリストで返す
def search_folder( A ):
    
    return glob.glob( A + "/*" )



    


def main():

    list_path = []
    list_label = []
    list_pair = [["file","label"]]

    
    #inputの中のフォルダを探索，そのパスをlabelに格納
    label = search_folder("./input")
    
    #keyに格納されたパスから"/"を取り除いてファイル名を取り出す
    for i in label:
        local_A = i.split("/")[-1]
        list_label.append( local_A )
        
    #ラベルの種類数を格納(クラス数)
    label_num = len(list_label)
    
    print("ラベル数：{}".format(label_num))
        

    for i in list_label:
    
        #フォルダ1つの中のファイルを探索(１つのラベルの中にどれだけファイルが入っているか)
        local_path = search_folder("./input" + "/" + str(i))
        
        for j in local_path:
        
            list_pair.append( [j, i] )
       
       
    #scvファイルに書き出し
    with open('sample.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows( list_pair )


            
        





if __name__ == "__main__":
    main()


