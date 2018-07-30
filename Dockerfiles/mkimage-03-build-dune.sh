#!/bin/bash

set -e

cd $HOME/parabolic-lrbms-2017-code/arch-full
export OPTS=gcc-relwithdebinfo
source PATH.sh
cd ..

nice ionice ./dune-common/bin/dunecontrol --opts=config.opts/$OPTS \
    --builddir=$INSTALL_PREFIX/../build-$OPTS all

