CRI?=podman
PROJ?=pic-compiler
ARM64IMAGE?=docker.io/pashi/pic-compiler-arm64
AMD64IMAGE?=docker.io/pashi/pic-compiler-amd64

readme:
	echo read Makefile

container:
	${CRI} build -t pic-compiler -f Containerfile . --no-cache

push_arm64:
	${CRI} tag pic-compiler ${ARM64IMAGE}
	${CRI} push ${ARM64IMAGE}

push_amd64:
	${CRI} tag pic-compiler ${AMD64IMAGE}
	${CRI} push ${AMD64IMAGE}

sync:
	rsync -vae ssh . srv01:src/${PROJ}
