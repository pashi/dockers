CRI?=podman
PROJ?=pic-compiler

readme:
	echo read Makefile

container:
	${CRI} build -t pic-compiler -f Containerfile . --no-cache

sync:
	rsync -vae ssh . srv01:src/${PROJ}
