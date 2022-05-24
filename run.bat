:: Run ETH Service on windows via powershell
docker run -it --rm --network=ethnet --ip=192.168.142.100 pythondev python /home/dev/service.py

:: Launch Grafana Web Interface
start "" http://localhost:3000
