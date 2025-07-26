#!/bin/sh

cd ..

docker rmi sttt
docker build -t sttt:latest -f ./docker/Dockerfile .
