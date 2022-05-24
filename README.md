# ETH-TX-Service

## Prerequisites
* Docker installed on host operating system

## Windows Instructions
Navigate to the **eth-tx-service** root directory.

- From powershell run cmd **.\bootstrap.bat**
  - This will provision a postgres database and grafana web service
- From powershell run cmd **.\run.bat**
  - This will run the service script within a python environment
  - As a user, you may 
    - Enter new addresses to scan
    - Enter new page numbers
    - Enter a new offset
  - Upon exit the script will launch the host machines web browser so that the transactions results can be visualized from within grafana
    - Grafana default login **admin:admin**
- From powershell run cmd **.\shutdown.bat**
  - This will turn off the infrastructure services
- From powershell run cmd **.\uninstall.bat**
  - This will remove all containers, volumes, images, networks that were provisioned by these scripts

  
## Linux Instructions
Navigate to the **eth-tx-service** root directory.

- From powershell run cmd **./bootstrap.sh**
  - This will provision a postgres database and grafana web service
- From powershell run cmd **./run.sh**
  - This will run the service script within a python environment
  - As a user, you may 
    - Enter new addresses to scan
    - Enter new page numbers
    - Enter a new offset
  - Upon exit the script will launch the host machines web browser so that the transactions results can be visualized from within grafana
    - Grafana default login **admin:admin**
- From powershell run cmd **./shutdown.sh**
  - This will turn off the infrastructure services
- From powershell run cmd **./uninstall.sh**
  - This will remove all containers, volumes, images, networks that were provisioned by these scripts

  

## Project Future Roadmap
* Security missing across the board
* More types of data sources to make more interesting correlations.
* CI/CD Scripting when/if the project reaches a sufficient size
* The 'service' is a dumb command line driven interface which is absolutely impractical but satisfies the project's basic needs.  A more sophisticated presentation/wizard would scale more organically with business needs.
* Setup Grafana alerts and integrations
* Investigate alternative visualization and monitoring frameworks
