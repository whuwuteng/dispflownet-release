# DispNetC on CNES HAL


## Introduction

There a some tricks for the [Docker](https://www.docker.com/) and [singularity](https://hpc.nih.gov/apps/singularity.html) especially with CUDA code.

## Dockerfile

Considering that the official caffe code is not supported the CuDNN 8(there is a way to change it, you can replace the **cudnn_conv_layer_cudnn8.cpp**), so the base environment is :
```
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
```

Important thing is that because the code need to be build, so the **devel version** is important. For example, if you just use the **Pytorch** code, you can use the **runtime version**.

## Folder permission

The command **ADD** and **COPY** can not change the permission. In the code, there are sub folders in the directory, if you want to run the code in the sub folder, the permission needs to be changed :
```
RUN chmod -R 777 ${tool}/models
```

## singularity

On the HAL, after building the image, you can run the image by :
```
singularity run --nv --writable-tmpfs dispflownet.img
```

**--nv** is to use the CUDA, and **--writable-tmpfs** is to write some temp files because the **demo.py** needs to write some files in the folder.

## Contact

If you think you have any problem, contact [Teng Wu]<whuwuteng@gmail.com>

 
