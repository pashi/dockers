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


readme:
	echo read Makefile

fetch:
	git clone https://github.com/psmay/pk2cmd.git||(cd pk2cmd && git pull)

debian12:
	${CRI} build -t pk2cmd -f Containerfile.debian12 .

debian13:
	#${CRI} build -t pk2cmd -f Containerfile.debian13 .
	VERSION=debian13 TAG=debian13 ARCH=${ARCH} make debian

debian: fetch
	${CRI} build -t ${REPOPREFIX}/${NAME}:${TAG} -f Containerfile.${VERSION} .

push:
	${CRI} push --platform linux/${CRI_ARCH} ${REPOPREFIX}/${NAME}:${TAG}

push-debian13:
	VERSION=debian13 TAG=debian13 ARCH=${ARCH} make push
