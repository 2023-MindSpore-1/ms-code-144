#!/usr/bin/env python
# coding: utf-8

# from mindvision.dataset import Mnist
import mindspore.nn as nn
from DataSet import MyDatasets

from models import *
from cell import *
import sys
import numpy as np
from tqdm import tqdm
# ========================================================

def test():
    # 读取数据集
    print('Test dataset loading ...')
    Art_DataSet = mindspore.dataset.GeneratorDataset(MyDatasets(data_path = '../DataSet/PACS/art_painting'), column_names=["image", "label"])
    Art_DataSet = Art_DataSet.batch(256)
    Cartoon_DataSet = mindspore.dataset.GeneratorDataset(MyDatasets(data_path = '../DataSet/PACS/cartoon'), column_names=["image", "label"])
    Cartoon_DataSet = Cartoon_DataSet.batch(256)
    Sketch_DataSet = mindspore.dataset.GeneratorDataset(MyDatasets(data_path = '../DataSet/PACS/sketch'), column_names=["image", "label"])
    Sketch_DataSet = Sketch_DataSet.batch(256)
    print('>> load finished!')

    # 读取模型
    net_test = AlexNet(num_classes=7)

    net_dict = mindspore.load_checkpoint('./SaveModel/model_PACS_P.ckpt')
    # for name, param in net_dict.items():
    #     if not name.startswith('optimizer.'):
    #         ms.load_param_into_net(net_test, net_dict)
    param_not_load = mindspore.load_param_into_net(net_test, net_dict)
    print('Model loading...')
    
    # 测试数据迭代
    test_number = 0
    correct_number = 0
    all_picture = 0
    for data in Art_DataSet.create_dict_iterator():
        test_number += 1
        
        img_T = data["image"]
        label_T = data["label"]

        onehot_label = net_test(img_T)

        pre_label = np.argmax(onehot_label, axis=1)
        
        correct_number += sum(pre_label == label_T)

        all_picture += len(pre_label)
    
        # if (test_number%100 == 0):
        #     print('已测试：\t', test_number)
        
    acc  = correct_number / all_picture
    print("DataSet P->A Accuracy is {:.2f}%".format(acc*100))

    test_number = 0
    correct_number = 0
    all_picture = 0
    for data in Cartoon_DataSet.create_dict_iterator():
        test_number += 1
        
        img_T = data["image"]
        label_T = data["label"]

        onehot_label = net_test(img_T)

        pre_label = np.argmax(onehot_label, axis=1)
        
        correct_number += sum(pre_label == label_T)

        all_picture += len(pre_label)
    
        # if (test_number%100 == 0):
        #     print('已测试：\t', test_number)
        
    acc  = correct_number / all_picture
    print("DataSet P->C Accuracy is {:.2f}%".format(acc*100))

    test_number = 0
    correct_number = 0
    all_picture = 0
    for data in Sketch_DataSet.create_dict_iterator():
        test_number += 1
        
        img_T = data["image"]
        label_T = data["label"]

        onehot_label = net_test(img_T)

        pre_label = np.argmax(onehot_label, axis=1)
        
        correct_number += sum(pre_label == label_T)

        all_picture += len(pre_label)
    
        # if (test_number%100 == 0):
        #     print('已测试：\t', test_number)
        
    acc  = correct_number / all_picture

    print("DataSet P->S Accuracy is {:.2f}%".format(acc*100))

if __name__ == "__main__":
    # 进行测试
    print('>>start test')
    test()
    print('>>测试完成')