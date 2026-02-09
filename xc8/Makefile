CRI?=podman
PROJ?=xc8

readme:
	echo read Makefile

fetch:
	curl -o xc8-v3.10-full-install-linux-x64-installer.run https://ww1.microchip.com/downloads/aemDocuments/documents/DEV/ProductDocuments/SoftwareTools/xc8-v3.10-full-install-linux-x64-installer.run
	chmod +x xc8-v3.10-full-install-linux-x64-installer.run

container:
	${CRI} build -t xc8 -f Containerfile .

sync:
	rsync -vae ssh . srv01:src/${PROJ}
