CRI?=podman

CRI_IMAGE ?= docker.io/pashi/dot
ARCH := $(shell uname -m)
ifeq ($(ARCH), aarch64)
    CRI_ARCH := arm64
else ifeq ($(ARCH), x86_64)
    CRI_ARCH := amd64
else ifeq ($(ARCH), arm64) # darwin
    CRI_ARCH := arm64
else
    $(error Unknown arch: $(ARCH))
endif

readme:
	echo read Makefile

build:
	${CRI} build -t ${CRI_IMAGE} -f Containerfile .

push:
	${CRI} push --platform linux/${CRI_ARCH} ${CRI_IMAGE}
