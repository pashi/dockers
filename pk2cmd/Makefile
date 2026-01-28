CRI?=podman
REPOPREFIX=docker.io/pashi
NAME=pk2cmd
VERSION?=none
TAG?=none

ARCH ?= $(shell uname -m)
ifeq ($(ARCH), aarch64)
    CRI_ARCH := arm64
else ifeq ($(ARCH), x86_64)
    CRI_ARCH := amd64
else ifeq ($(ARCH), arm64) # darwin
    CRI_ARCH := arm64
else
    $(error Tuntematon arkkitehtuuri: $(ARCH))
endif

ifeq ($(CRI), docker)
	PUSH_PARAMS :=  --platform linux/${CRI_ARCH} 
else ifeq ($(ARCH), podman)
    PUSH_PARAMS :=
else
	PUSH_PARAMS :=
endif


readme:
	echo read Makefile

fetch:
	git clone https://github.com/psmay/pk2cmd.git||(cd pk2cmd && git pull)

debian12:
	VERSION=debian12 TAG=debian12 ARCH=${ARCH} make debian

debian13:
	VERSION=debian13 TAG=debian13 ARCH=${ARCH} make debian

debian: fetch
	${CRI} build --platform linux/${CRI_ARCH} -t ${REPOPREFIX}/${NAME}-${CRI_ARCH}:${TAG} -f Containerfile.${VERSION} .

push:
	${CRI} push ${PUSH_PARAMS} ${REPOPREFIX}/${NAME}-${CRI_ARCH}:${TAG}

push-debian12:
	VERSION=debian12 TAG=debian12 ARCH=${ARCH} make push

push-debian13:
	VERSION=debian13 TAG=debian13 ARCH=${ARCH} make push

clean:
	rm -rf pk2cmd
