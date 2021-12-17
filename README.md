# AASD_ZespolX

## Prerequisites:
- docker
- miniconda or conda

## Setup:
1. Import environment with conda prompt `conda env create -f environment.yml`
1. Run startup.ps1 from project folder to start prosody docker container
1. Enter prosody container `docker exec -it prosody bash`
1. Run `sh setup.sh` (don't bother about errors)

## Run
* Run `python src/main.py` in imported conda environment

## About

setup.sh - Contains xmpp account registrations for agents. If you want to create new agent you have to specify account for it in this file and run it from container again.
