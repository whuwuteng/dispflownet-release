# load folder list 

import os
import argparse
import os.path
import random
from PIL import Image
import numpy as np

from readwritepfm import read_pfm, write_pfm 

import pdb

# not finished
def LoadList(file) :
    all_left_img = []
    all_right_img = []
    all_disp_img = []

    with open(file) as w :
        content = w.readlines()
        content = [x.strip() for x in content] 
        for line in content :
            if line :
                file = line.split()
                all_left_img.append(file[0])
                all_right_img.append(file[1])
                all_disp_img.append(file[2])

    return all_left_img, all_right_img, all_disp_img

def SamplePFM(src, tar, sample) :
    disp_png, scale = read_pfm(src)
    d_height, d_width= disp_png.shape

    #print(d_width)

    v_coord = random.choices(range(d_height), k=sample)
    u_coord = random.choices(range(d_width), k=sample)

    disp_pfm = np.ones((d_height, d_width), dtype=np.float32) * np.nan
    disp_pfm[v_coord[:], u_coord[:]] = disp_png[v_coord[:], u_coord[:]]

    write_pfm(tar, disp_pfm)

# in order to adapt with other dataset
# only keep the left image
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make training and test file list')

    # folder list file is in the data path
    
    parser.add_argument('--src', type=str, default=None, help='training data folder list')
    parser.add_argument('--tar', type=str, default=None, help='training data folder list')
    parser.add_argument('--sample', type=int, default=32400, help='sample number')
    
    
    args = parser.parse_args()

    left_img, right_img, disp_img = LoadList(args.src)

    disp_pfm = []

    for disp in disp_img :
    #disp = disp_img[0]
        print(disp)
        pre, ext = os.path.splitext(disp)
        pfm = pre + '_sample.pfm'

        SamplePFM(disp, pfm, args.sample)
        disp_pfm.append(pfm)

    disp_img = disp_pfm

    #exit()
    
    num = len(left_img)
    with open(args.tar, "w") as output:
        for i in range(0, num) :
            output.write(left_img[i] + ' ' + right_img[i] + ' ' + disp_img[i] + '\n')
