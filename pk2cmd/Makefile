CRI?=podman

readme:
	echo read Makefile

fetch:
	git clone https://github.com/psmay/pk2cmd.git

debian12:
	${CRI} build -t pk2cmd -f Containerfile.debian12 .

debian13:
	${CRI} build -t pk2cmd -f Containerfile.debian13 .

