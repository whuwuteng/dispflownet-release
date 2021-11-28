#! /bin/bash


LIST="/home/tengwu/dataset/stereodensematchingbenchmark/Vaihingen-stereo_echo/training/"
DIR1="/home/tengwu/dataset/stereodensematchingbenchmark/Vaihingen-stereo_echo/"
python3 make_trainlist.py --folderlist ${LIST}/train_folderlist.txt --trainlist ${DIR1}/vaihingen_trainlist_dispnet.txt --vallist ${DIR1}/vaihingen_vallist_dispnet.txt \
--pfm 

#LIST="/home/tengwu/dataset/stereobenchmark/kitti2015/"
#DIR1="/home/tengwu/dataset/stereobenchmark/kitti2015/"
#python3 make_trainlist.py --folderlist ${LIST}/train.txt --trainlist ${DIR1}/kitti_trainlist_dispnet.txt --vallist ${DIR1}/kitti_vallist_dispnet.txt \
#--pfm 




#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/EuroSDR_vaihingen-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/train_folderlist.txt --trainlist ${DIR1}/eurosdr_vaihingen_trainlist.txt --vallist ${DIR1}/eurosdr_vaihingen_vallist.txt

#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/Enschede-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/train_folderlist.txt --trainlist ${DIR1}/enschede_trainlist.txt --vallist ${DIR1}/enschede_vallist.txt

#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/Enschede-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/folder_selected.txt --trainlist ${DIR1}/enschede_trainlist.txt --trainnum 1200 --vallist ${DIR1}/enschede_vallist.txt --valnum 200


#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/DublinCity-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/train_folderlist.txt --trainlist ${DIR1}/dublin_trainlist.txt --trainnum 1200 --vallist ${DIR1}/dublin_vallist.txt --valnum 200

#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/Toulouse_UMBRA-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/train_folderlist.txt --trainlist ${DIR1}/toulouse_trainlist.txt --trainnum 1200 --vallist ${DIR1}/toulouse_vallist.txt --valnum 200
#python3 make_trainlist.py --folderlist ${DIR1}/folderlist.txt --ratio 0.9 --trainnum 478 --trainlist ${DIR1}/toulouse_trainlist_478.txt --valnum 119 --vallist ${DIR1}/toulouse_vallist_119.txt

#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/IARPA-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/folderlist.txt --ratio 0.9 --trainnum 100 --trainlist ${DIR1}/IARPA_trainlist_100.txt --valnum 10 --vallist ${DIR1}/IARPA_vallist_10.txt

#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/IARPA-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/folderlist.txt --trainlist ${DIR1}/iarpa_cbmv.txt --trainnum 54

#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/Toulouse_TlseMetro-stereo_echo/training"
#python3 make_trainlist.py --folderlist ${DIR1}/train_folderlist.txt --trainlist ${DIR1}/toulouse_tlse_trainlist.txt --trainnum 1200 --vallist ${DIR1}/toulouse_tlse_vallist.txt --valnum 200



# new train method
#LIST="/home/qt/tengw/scratch/Toulouse_UMBRA/experiment_echo_train/train_list.txt"
#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/Toulouse_UMBRA-stereo_echo_new/training/"

#python3 make_trainlist.py --folderlist ${DIR1}/folderlist.txt --trainlist ${DIR1}/toulouse_trainlist.txt --trainnum 1200 --vallist ${DIR1}/toulouse_vallist.txt --valnum 200

#LIST="/home/qt/tengw/scratch/Enschede/experiment_echo_train/PSMnet_train_list.txt"
#DIR1="/work/OT/ai4geo/users/tengw/stereodensematchingbenchmark/Enschede-stereo_echo/training/"
#python3 make_trainlist.py --folderlist ${LIST} --full --trainlist ${DIR1}/enschede_trainlist.txt --trainnum 800 --vallist ${DIR1}/enschede_vallist.txt --valnum 200
