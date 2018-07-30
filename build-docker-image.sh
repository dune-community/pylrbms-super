#!/bin/bash

pushd Dockerfiles
sudo docker build --rm=true --force-rm=true -t ftschindlerwork/parabolic-lrbms-2017 \
    -f Dockerfile .
popd
