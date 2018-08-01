FROM dunecommunity/testing-base_debian:latest

# COMPILER Selection (ARGS cannot be uppercase)
ARG cc
ARG cxx
ARG commit
ARG URL
ENV CC=$cc \
    CXX=$cxx \
    MY_MODULE=pylrbms

WORKDIR ${SUPERDIR}
RUN git config --global credential.helper cache && \
    echo "username=r_milk01\nprotocol=https\nhost=zivgitlab.uni-muenster.de\npassword=$(wget -qO- ${URL}/token)\n\n" \
        | git credential approve && \
    ${DUNE_VENV_ACTIVATE} && \
    git clone https://github.com/dune-community/pylrbms-super.git ${SUPERDIR} && \
    git checkout ${commit} && \
    cd ${SUPERDIR} && \
    git submodule foreach git reset --hard && \
    git submodule update --init --recursive && \
    ./bin/download_external_libraries.py && \
    ./bin/build_external_libraries.py && \
    ${SRC_DCTRL} ${BLD} all && \
    ${SRC_DCTRL} ${BLD} --only=${MY_MODULE} bexec ${BUILD_CMD} dependent_bindings && \
    rm -rf ${MY_MODULE} && \
    mkdir ${MY_MODULE}

# THE END
ENV DEBIAN_FRONTEND teletype
