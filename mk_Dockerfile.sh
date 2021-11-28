#! /bin/bash 

vs=0.0

# build
sudo docker image build -t dispflownet:${vs} .

#set 
#sudo docker tag micmac_tool:${vs} whuwuteng/micmac_tool:${vs}

# push
#sudo docker push whuwuteng/micmac_tool:${vs}
