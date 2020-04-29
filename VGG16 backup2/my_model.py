#/usr/bin/env python
#coding: utf-8
#from ファイルパス import 関数名


import glob
import numpy as np
from chainer import cuda, Variable, optimizers, Chain
import chainer
import chainer.functions as F
import chainer.links as L
from chainer.training import extensions


#VGG16
class Model_VGG16(chainer.Chain):
    
    def __init__(self, out_size):
        
        super(Model_VGG16, self).__init__( vgg = L.VGG16Layers(), fc = L.Linear( None, out_size ) )
    
    def __call__(self, x, extract_feature=False):
        
        h = self.vgg( x, layers = ["fc7"] )["fc7"]
        
        
        if extract_feature:
            return h
        
        
        y = self.fc(h)
        return y



#ResNet152
class Model_ResNet(chainer.Chain):

    def __init__(self, out_size):
        super(Model_ResNet, self).__init__(base = L.ResNet152Layers(),fc = L.Linear(None, out_size))

    def __call__(self, x):
        h = self.base(x, layers=['pool5'])
        y = self.fc(h['pool5'])
        return y
