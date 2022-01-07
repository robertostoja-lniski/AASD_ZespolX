# AASD_ZespolX

## Prerequisites:
- docker
- miniconda or conda

## Setup:
1. Import environment with conda prompt `conda env create -f environment.yml`
1. Run startup.ps1 from project folder to start prosody docker container
1. Enter prosody container `docker exec -it prosody bash`
1. Run `./setup.sh` (don't bother about errors)

## Run
* Run `python -m src.main` in imported conda environment

Parameters:
```
 --n_fisheries - liczba łowisk
```

## Usage
When the program is running you can press one of the following keys:
* q - quit the program
* f - generate recommendation. Recommendation will appear as a new file at <cwd>/recommendations/<user_JID> almost instantly.
* r - generate report

## About

prosody/accounts.sh - Contains xmpp account registrations for agents. If you want to create new agent you have to specify account for it in this file and run it from container again.
