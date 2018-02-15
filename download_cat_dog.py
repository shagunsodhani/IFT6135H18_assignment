#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 13:31:59 2018

@author: chinwei
"""

import urllib
import cPickle as pickle
import gzip
import os
import numpy as np
import zipfile
import scipy.ndimage


final_size = 64


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--savedir', type=str, default='datasets', 
                        help='directory to save the dataset')
    args = parser.parse_args()

    if not os.path.exists(args.savedir):
        os.makedirs(args.savedir)

    urlpath = 'https://storage.googleapis.com/kaggle-competitions-data/kaggle/3362/train.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1518904543&Signature=G/fKHaGZzD7CAe18uadQaIll1rqvHXDbZqiFWke7qkRSqiAFrphNnay5e/hqX1A8yJaOLHRPOYWZaRSfRMozu1DL2nwM6clNAGqjsXuDtiA6Xkub%2Bz99Bj40wfnhn95EMPL5d/fgp6ZUB%2BZ/5MNbsf1VQiJEDg9qsUTXSJ6SWEQesHGYpxz8FymSP1DzLAjQdYOuGiUOup90PCCAfBzo0FCE0zxPZcw3NUYTS3IiJNJlAa2tkAvgvFHxEk77HIyfj/tnJ0Sm8%2BDHbzXnCVI3UgUDnQ1LGF4YWoEEL%2BCvNtKzCZr4Dw/zBaiRQcS5WMziFYNPv%2B3KQtT7B0vwLY3ENA%3D%3D'
    filename  = 'train.zip'
    filepath = os.path.join(args.savedir, filename)
    print "Downloading..."
    urllib.urlretrieve(urlpath, filepath)

    print "Extracting file..."
    zip_ref = zipfile.ZipFile(filepath, 'r')
    zip_ref.extractall(args.savedir)
    zip_ref.close()

    train_data = os.path.join(args.savedir, 'train')
    train_proc_data = os.path.join(args.savedir, 'train_64x64')
    if not os.path.exists(train_proc_data):
        os.makedirs(train_proc_data)

    for pic_file in os.listdir(train_data):
        pic_path = os.path.join(train_data, pic_file)
        img = scipy.ndimage.imread(pic_path)
        side_dim = min(img.shape[0], img.shape[1])
        start_height = (img.shape[0] - side_dim) // 2
        start_width = (img.shape[1] - side_dim) // 2
        img = img[start_height: start_height + side_dim,
                  start_width: start_width + side_dim]
        img = scipy.misc.imresize(
            img,
            size=float(final_size) / img.shape[0],
            interp='bilinear'
        )


        if (img.shape[0] != final_size or
            img.shape[1] != final_size):
            img = img[:final_size, :final_size]



        scipy.misc.imsave(
            os.path.join(train_proc_data, pic_file),
            img
        )

