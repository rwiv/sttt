#!/bin/sh

cd ..
sudo docker compose -f ./docker/docker-compose-prod.yml rm
sudo docker compose -f ./docker/docker-compose-prod.yml up -d
