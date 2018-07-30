#!/bin/bash

set -e

cd $HOME/parabolic-lrbms-2017-code/arch-full
export OPTS=gcc-relwithdebinfo
source PATH.sh
cd ..

./local/bin/download_external_libraries.py
./local/bin/build_external_libraries.py

