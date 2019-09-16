#/usr/bin/env python
#coding: utf-8



#ブレインだーライブラリ（日本語を使うな）
import bpy



def main():


    #レンダリングしてイメージを保存
    bpy.ops.render.render()

    bpy.data.images["Render Result"].save_render( filepath = "./img/0001.png" )

        
        
        







if __name__ == "__main__":
    main()


