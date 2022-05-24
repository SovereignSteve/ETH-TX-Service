#! /bin/bash

# Build Images
cd Dockerfiles
./build-all.sh

# Prepare Network
docker network create --driver=bridge --subnet=192.168.142.0/24 ethnet

# Launches Infrastructure Services
docker run -itd --name=postgres-eth-service --network=ethnet --ip=192.168.142.80 -p 5432:5432/tcp postgres-eth-service
docker run -itd --name=grafana-eth-service --network=ethnet --ip=192.168.142.90 -p 3000:3000/tcp grafana-eth-service
