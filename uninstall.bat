call shutdown.bat

docker rm -v grafana-eth-service
docker rm -v postgres-eth-service
docker rmi grafana-eth-service
docker rmi postgres-eth-service
docker rmi pythondev

docker network rm ethnet
