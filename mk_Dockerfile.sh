#! /bin/bash 

vs=0.0

# build
sudo docker image build -t dispflownet:${vs} .

#set 
sudo docker tag dispflownet:${vs} whuwuteng/dispflownet:${vs}

# push
sudo docker push whuwuteng/dispflownet:${vs}
