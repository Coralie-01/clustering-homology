#!/bin/bash

#check if docker is installed and print version

if [ -x "$(command -v docker)" ]; then
    echo "Docker is installed"
    docker --version
else
    echo "Docker is not installed"
fi
