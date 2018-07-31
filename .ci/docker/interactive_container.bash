DIR="$(cd "$(dirname ${BASH_SOURCE[0]})" ; cd ../../ ; pwd -P )"

docker run --rm -it -v ${DIR}/pylrbms:/root/src/pylrbms dunecommunity/pylrbms-testing_gcc:master bash
