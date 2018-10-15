FROM dunecommunity/testing-base_debian:latest

# COMPILER Selection (ARGS cannot be uppercase)
ARG cc
ARG cxx
ARG commit
ARG URL
ENV CC=$cc \
    CXX=$cxx \
    MY_MODULE=pylrbms

# this should not be necessary, but /home/dune-ci/src is root-owned for some reason
USER root
RUN chown -R dune-ci /home/dune-ci/
USER dune-ci

RUN /bin/bash -c 'set -ue && export ZIVGITLAB_TOKEN="$(wget -qO- ${URL}/token)" && \
    git config --global url."https://r_milk01:${ZIVGITLAB_TOKEN}@zivgitlab.uni-muenster.de/".insteadOf https://zivgitlab.uni-muenster.de/ && \
    git clone https://github.com/dune-community/pylrbms-super.git ${SUPERDIR} && \
    cd ${SUPERDIR} && \
    git checkout ${commit} && \
    git submodule foreach git reset --hard && \
    git submodule update --init --recursive && \
    ./bin/download_external_libraries.py && \
    ./bin/build_external_libraries.py && \
    ${SRC_DCTRL} ${BLD} all && \
    ${SRC_DCTRL} ${BLD} --only=${MY_MODULE} bexec ${BUILD_CMD} dependent_bindings && \
    rm -rf ${MY_MODULE} && \
    mkdir ${MY_MODULE}'

VOLUME ${SUPERDIR}/${MY_MODULE}
