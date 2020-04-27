#/usr/bin/env python
#coding: utf-8
#from ファイルパス import 関数名

import glob
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt
from sklearn import manifold, metrics
from chainer import cuda, Variable, optimizers, Chain
import chainer
import chainer.functions as F
import chainer.links as L
from chainer.training import extensions
from PIL import Image
from tqdm import tqdm   #進捗状況をプログレスバーとして表示するやつ
import my_model




model_path = "result_VGG16_edge/snapshot_epoch-6"


# gpuを使いたくなければここをマイナス値に変える
gpu = 0

# csvを開く
df = pd.read_csv("train.csv")


# モデル，オプティマイザーの設定
model = L.Classifier( my_model.Model_VGG16( out_size = len( df["label"].unique() ) ) )

chainer.serializers.load_npz( model_path, model, strict = False )


#alpha = 1e-4
#optimizer = chainer.optimizers.Adam( alpha = alpha )
#optimizer.setup( model )

#model.predictor["fc"].W.update_rule.hyperparam.lr = alpha*10
#model.predictor["fc"].b.update_rule.hyperparam.lr = alpha*10


# 使うユニットをgpuに設定
if gpu >= 0:
    
    chainer.cuda.get_device(gpu).use()
    model.to_gpu(gpu)




# テストデータのcsvを開く
df = pd.read_csv("test.csv")

# 画像本体(pngファイル)のパスを作る
test_paths = "" +  df["file"].values

# .as_matrix()：numpy配列に変換する
test_labels = df["label"].values



ys_pre, ys, features = [], [], []

accNum = 0;
i = 0;
huseikai_path = []
huseikai_acc = []
huseikai_pre = []



for path, label in tqdm( zip( test_paths, test_labels ) ):
    
    img = Image.open(path)
    
    # 通常入力画像を(batchsize,channels,height,width)、channelsはRGBではなくBGRという形式のnumpyarrayに整形する また、256x256へリサイズ、224x224へクロップする作業、VGG16の平均画素[103.939, 116.779, 123.68]の引き算も同時に行う。
    img = L.model.vision.vgg.prepare(img)
    img = img[np.newaxis, :]
    img = cuda.to_gpu(img)
    
    y_pre = model.predictor(img)
    # dataの形状を予測変換( 1次元配列に変換 )
    y_pre = y_pre.data.reshape(-1)
    # 変換された配列の最大値( 最大スコア )のインデックスを得る
    y_pre = np.argmax(y_pre)

    
    #何回ループしたかを観測
    i = i + 1
    
    # 正解していたらaccNumを加算
    if( y_pre == label ):
        accNum = accNum + 1;
    else:
        huseikai_path.append( path.split("/")[-1] )
        huseikai_pre.append( y_pre )
        huseikai_acc.append( label )



# 正解率の計算
acc = accNum / i

for j in range( len(huseikai_path) ):
    print(" 不正解情報ー予想：{}  正解：{}  番号：{}" .format( huseikai_pre[j], huseikai_acc[j], huseikai_path[j] ))


print("")
print("正解率 : {} %   ( {} / {} )" . format( acc * 100, accNum, i ) )
print("")
print("")


ys = np.array(ys, dtype=np.int32)
ys_pre = np.array(ys_pre, dtype=np.int32)
features = np.array(features, dtype=np.float32)

# feature :　直訳ー特徴












