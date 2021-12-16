# AASD_ZespolX

## Prerequisites:
- docker
- miniconda or conda

## How to run
1. Import environment with conda prompt `conda env create -f environment.yml`
1. Run startup.ps1 to start prosody docker container
1. Enter prosody container `docker exec -it prosody bash`
1. Run `sh setup.sh` (don't bother about errors)
1. Run main.py in imported conda environment
1. Enjoy