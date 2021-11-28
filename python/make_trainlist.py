# load folder list 

import os
import argparse
import os.path
import random
from PIL import Image
import numpy as np

from readwritepfm import write_pfm 

import pdb

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def dataloader(folderlist):
    path, filename = os.path.split(folderlist)

    folder = []
    with open(folderlist) as w :
        content = w.readlines()
        content = [x.strip() for x in content] 
        for line in content :
            if line :
                folder.append(line)

    #  kitti
    """left_fold  = 'image_2/'
    right_fold  = 'image_3/'
    disp_fold  = 'disp_occ_0/'
    """
    # aerial
    
    left_fold  = 'colored_0/'
    right_fold  = 'colored_1/'
    disp_fold  = 'disp_occ/'


    all_left_img = []
    all_right_img = []
    all_disp_img = []

    for subfolder in folder :
        filepath =  path + '/' + subfolder + '/'
        image = [img for img in os.listdir(filepath+disp_fold) if is_image_file(img)]
        train = image[:]

        left_train  = [path + '/' + subfolder + '/' + left_fold + img for img in train]
        right_train  = [path + '/' + subfolder + '/' + right_fold + img for img in train]
        disp_train  = [path + '/' + subfolder + '/' + disp_fold + img for img in train]
        
        all_left_img = all_left_img + left_train
        all_right_img = all_right_img + right_train
        all_disp_img = all_disp_img + disp_train
    return all_left_img, all_right_img, all_disp_img

# not finished
def LoadList(file) :
    filelist = []
    with open(file) as w :
        content = w.readlines()
        content = [x.strip() for x in content] 
        for line in content :
            if line :
                filelist.append(line)

    return filelist


def ConvertPNG2PFM(png, pfm, scale) :
    disp_png = Image.open(png)

    d_width, d_height = disp_png.size
    disp_png = np.array(disp_png)

    mask_nan = (disp_png == 0)
    mask = (disp_png > 0)

    print("valid pixels: " + str(mask.sum()))

    disp_pfm = np.zeros((d_height, d_width), dtype=np.float32)

    disp_pfm[mask_nan] = np.nan
    disp_pfm[mask] = disp_png[mask]/scale
    
    disp_pfm = np.flipud(disp_pfm)

    write_pfm(pfm, disp_pfm)

# in order to adapt with other dataset
# only keep the left image
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make training and test file list')

    # folder list file is in the data path
    
    parser.add_argument('--folderlist', type=str, default=None, help='training data folder list')
    parser.add_argument('--full', action='store_true', default=False, help='use full left image list')

    parser.add_argument('--ratio', type=float, default=0.8, help='ratio for training data and valuation data')
    parser.add_argument('--trainnum', type=int, default=100, help='max training sample number')
    parser.add_argument('--trainlist', type=str, default=None, help='save training file list')
    parser.add_argument('--valnum', type=int, default=20, help='max evluation sample number')
    parser.add_argument('--vallist', type=str, default=None, help='validation data path')
    
    parser.add_argument('--disp_scale', type=float, default=256, help='disparity image is scaled')
    parser.add_argument('--pfm', action='store_true', default=False, help='save disparity as pfm')
    
    args = parser.parse_args()

    #if args.full :
    #    left_img, right_img, disp_img = LoadList(args.folderlist)
    #else :
    left_img, right_img, disp_img = dataloader(args.folderlist)

    disp_pfm = []
    if args.pfm :
        #for disp in disp_img :
        disp = disp_img[0]
        print(disp)
        pre, ext = os.path.splitext(disp)
        pfm = pre + '.pfm'

        ConvertPNG2PFM(disp, pfm, args.disp_scale)
        disp_pfm.append(pfm)

        disp_img = disp_pfm

    exit()

    num = len(left_img)

    train_num = int(num * args.ratio + 0.5)
    val_num = num - train_num

    if args.trainnum > 0:
        train_num =  min(train_num, args.trainnum)

    if args.valnum > 0 :
        val_num = min(val_num, args.valnum)

    # bug for dispnet data
    #random.shuffle(left_img)

    if args.trainlist :
        with open(args.trainlist, "w") as output:
            for i in range(0, train_num) :
                output.write(left_img[i] + ' ' + right_img[i] + ' ' + disp_img[i] + '\n')

    stop_num = train_num + val_num
    if args.vallist :
        with open(args.vallist, "w") as output:
            for i in range(train_num, stop_num) :
                output.write(left_img[i] + ' ' + right_img[i] + ' ' + disp_img[i] + '\n')
