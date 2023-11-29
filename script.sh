#!/usr/bin/env bash

curl -fsSL https://get.docker.com/ -o get-docker.sh
sudo sh get-docker.sh

sudo docker compose up -d
