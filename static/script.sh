#!/usr/bin/env bash

if [ ! -x "$(command -v docker)" ]; then
    curl -fsSL https://get.docker.com/ -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

sudo docker compose up -d
