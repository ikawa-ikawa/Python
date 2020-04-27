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





# csvを開く
df = pd.read_csv("train.csv")

# 画像本体(pngファイル)のパスを作る
train_paths = "" + df["file"].values

# .values()：numpy配列に変換する
train_labels = df["label"].values


dataset = []

# データセットに画像本体とラベルを追加する
for path, label in tqdm( zip( train_paths, train_labels ) ):
    
    # 画像を開く
    img = Image.open(path)
    # 前処理
    img = L.model.vision.vgg.prepare(img)
    # ラベルをint32型に変換
    label = np.int32(label)
    # データセットに画像データとラベルを追加
    dataset.append( (img, label) )

# データセットの長さを得る（データ分割時に使用）
N = len(dataset)


# gpuを使いたくなければここをマイナス値に変える
gpu = 0



# モデル，オプティマイザーの設定
model = L.Classifier( my_model.Model_VGG16( out_size = len( df["label"].unique() ) ) )
alpha = 1e-4
optimizer = chainer.optimizers.Adam( alpha = alpha )
optimizer.setup( model )

model.predictor["fc"].W.update_rule.hyperparam.lr = alpha*10
model.predictor["fc"].b.update_rule.hyperparam.lr = alpha*10


# 使うユニットをgpuに設定
if gpu >= -1:
    
    chainer.cuda.get_device(gpu).use()
    model.to_gpu(gpu)




# ----------データの分割と学習----------
print("")
print("Start learn")

epoch_num = 10
batch_size = 16

# データセットを学習データとテストデータに分割する（ランダム選択）第一引数：データセット本体　第二引数：学習データの割合
split_at = int( len( dataset ) * 0.8 )
train, valid = chainer.datasets.split_dataset_random(dataset, split_at )



print("train_size = {}" .format( len(train) ))
print("valid_size = {}" .format( len(valid) ))

# バリデーションに選ばれた画像のラベルを取得，表示（このラベルが全部一緒になると学習がうまくいかない）
valid_labels = []
for i in range( len( valid ) ):
    valid_labels.append(valid[i][1])


# iterators.SerialIterator( dataset : 反復するデータ，  batch_size : バッチサイズ(int),   repeat = True-無限ループ False-全てのデータ(1エポック分)を返すと反復を終える)
train_iter = chainer.iterators.SerialIterator(train, batch_size)
valid_iter = chainer.iterators.SerialIterator(valid, batch_size, repeat=False, shuffle=False)

# アップデーターの設定
updater = chainer.training.StandardUpdater(train_iter, optimizer, device = gpu)

# chainer.training.Trainer(updater, stop_trigger = None, out='result' )
trainer = chainer.training.Trainer(updater, (epoch_num, "epoch"), out="result")




# Evaluator : 直訳ー評価者
trainer.extend( extensions.Evaluator( valid_iter, model, device = gpu ) )
# ログをファイルに出力する
trainer.extend( extensions.LogReport() )
# print文を使って現状をprintする
trainer.extend( extensions.PrintReport (["epoch", "main/loss", "validation/main/loss", "main/accuracy", "validation/main/accuracy", "elapsed_time"]) )

# ファイルに出力する
trainer.extend( extensions.PlotReport( ["main/loss", "validation/main/loss"], "epoch", file_name="loss.png") )
trainer.extend( extensions.PlotReport( ["main/accuracy", "validation/main/accuracy"], "epoch", file_name = "accuracy.png") )
# プログレスバーを表示する
trainer.extend(extensions.ProgressBar())

#モデルを吐く
trainer.extend(extensions.snapshot_object( model, "snapshot_epoch-{.updater.epoch}"))












trainer.run()

print("Fin learn")
print("")
