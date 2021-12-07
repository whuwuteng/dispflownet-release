# DispNetC on CNES HAL


## Introduction

There are some tricks for the [Docker](https://www.docker.com/) and [singularity](https://hpc.nih.gov/apps/singularity.html) especially with CUDA code. The DispNetC code is original from [dispnet-flownet-docker](https://github.com/lmb-freiburg/dispnet-flownet-docker).

[Someone says](https://stackoverflow.com/questions/57015346/can-i-run-a-docker-container-with-cuda-10-when-host-has-cuda-9) that the CUDA version should be same between the container and host, I am not sure, so I use the following setting.

## Dockerfile

Considering that the official caffe code doesnot support the CuDNN 8(there is a way to change it, you can replace the **cudnn_conv_layer_cudnn8.cpp**), so the base environment is :
```
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
```

The important thing is that because the code needs to be built, so the **devel version** is important. For example, if you just use the **Pytorch** code, you can use the **runtime version**.

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

 
