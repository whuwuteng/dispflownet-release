#! /bin/bash


#DIR1="/home/tengwu/dataset/FlyingThings3D_release"

DIR1="/home/whuwuteng/CodeProject/dispflownet-release/data"
python3 make_sample_trainlist.py --src ${DIR1}/FlyingThings3D_release_TRAIN_small.list \
--tar ${DIR1}/FlyingThings3D_release_TRAIN_small_sample.list 