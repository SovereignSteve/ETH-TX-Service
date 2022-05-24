#! /bin/bash

# Run ETH Service on linux
docker run -it --rm --network=ethnet --ip=192.168.142.100 pythondev python /home/dev/service.py

# Launch Grafana Web Interface
xdg-open https://stackoverflow.com