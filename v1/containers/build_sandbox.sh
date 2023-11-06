#!/bin/bash

# 2023 Lars Quentin

# Call it with
# ./scriptname ./path/to/your/Dockerfile
#
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ $# -ne 1 ]
  then echo "USAGE: ./scriptname ./path/to/your/Dockerfile"
  exit
fi


docker_filename="docker_$(date +%Y-%m-%d_%H-%M-%S).tar.gz"
singularity_filename="singularity_$(date +%Y-%m-%d_%H-%M-%S).sif"

sudo rm -rf docker_* singularity_*

docker save "$(sudo docker build -q -f $1 .)" -o $docker_filename && \
sudo singularity build --sandbox $singularity_filename docker-archive://$docker_filename

