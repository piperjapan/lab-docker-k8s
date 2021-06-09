#!/bin/bash

echo "* Add an alias for docker-compose to the shell configuration file ..."

echo alias docker-compose="'"'docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.29.2'"'" >> ~/.bashrc

echo "* Pull container image for docker-compose ..."
docker run --rm docker/compose:1.29.2 version

echo "* Done"
echo "* To use docker-compose, run 'source ~/.bashrc' or simply re-login"
