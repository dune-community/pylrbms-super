#!/bin/bash

set -e

cd $HOME
git clone https://zivgitlab.uni-muenster.de/falbr_01/parabolic-lrbms-2017-code.git
cd $HOME/parabolic-lrbms-2017-code
# this should be all but pymor (that one is private)
for ii in config.opts dune-alugrid dune-common dune-fem dune-functions dune-gdt dune-geometry \
        dune-grid dune-istl dune-localfunctions dune-pdelab dune-pybindxi \
        dune-python dune-testtools dune-typetree dune-xt-common dune-xt-functions \
        dune-xt-grid dune-xt-la local/bin; do
    git submodule update --init --recursive $ii;
done

export OPTS=gcc-relwithdebinfo

