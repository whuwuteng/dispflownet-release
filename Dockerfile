## Note: Our Caffe version does not work with CuDNN 6
## FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

## important
## refer to https://www.cnblogs.com/tl542475736/p/9645920.html
ARG DEBIAN_FRONTEND=noninteractive

## Put everything in some subfolder
ENV tool /etc/opt/dispflownet

WORKDIR ${tool}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        module-init-tools \
        build-essential \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-scipy

WORKDIR ${tool}
COPY ./include ${tool}/include
COPY ./matlab  ${tool}/matlab
COPY ./python  ${tool}/python
COPY ./scripts ${tool}/scripts
COPY ./src     ${tool}/src
COPY ./tools   ${tool}/tools
COPY ./models  ${tool}/models
RUN chmod -R 777 ${tool}/models
COPY ./examples   	${tool}/examples
COPY ./Makefile   	${tool}/
COPY ./Makefile.config	${tool}/
RUN make -j 5 all tools






