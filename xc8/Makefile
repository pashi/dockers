CRI?=podman
PROJ?=xc8
PACKDIR=packs
DLDIR:=downloads
XC8VERSION ?= 4.00
XC8DOWNLOADURL ?= https://ww1.microchip.com/downloads/aemDocuments/documents/DEV/ProductDocuments/SoftwareTools/xc8-v$(XC8VERSION)-full-install-linux-x64-installer.run
LOGFILE := /tmp/xc.log

# e.g.
# https://packs.download.microchip.com/Microchip.PIC10-12Fxxx_DFP.1.9.189.atpack

define fetch_microchip_pack
	mkdir -p $(PACKDIR)/$(1) $(DLDIR)/$(PACKDIR)
	curl -v -o $(DLDIR)/$(PACKDIR)/$(1).zip https://packs.download.microchip.com/Microchip.$(1).$(2).atpack
endef
#echo "Microchip.$(1).$(2).atpack" >> $(PACKDIR)/info.txt
#unzip $(DLDIR)/$(1).zip -d $(PACKDIR)/$(1)


.PHONY: readme fetch fetch-packs container clean clean-packs clean-download

readme:
	echo read Makefile

fetch: fetch-installer fetch-packs

fetch-installer:
	mkdir -p $(DLDIR)
	curl -o $(DLDIR)/xc8.run $(XC8DOWNLOADURL)
	chmod +x $(DLDIR)/xc8.run

fetch-packs:
	$(call fetch_microchip_pack,PIC16F1xxxx_DFP,1.31.465)
	$(call fetch_microchip_pack,PIC10-12Fxxx_DFP,1.9.189)

container:
	${CRI} build -t xc8 -f Containerfile .

sync:
	rsync -vae ssh . srv01:/tmp/${PROJ}

clean: clean-packs clean-download

clean-packs:
	rm -rf $(PACKDIR)

clean-download:
	rm -rf $(DLDIR)

update-public-dockers:
	echo 'sync from forgejo' > $(LOGFILE)
	git log -1 --pretty=%B >> $(LOGFILE)
	(cp * ../dockers/xc8/ && cd ../dockers/xc8/ && pwd && git commit . -F $(LOGFILE) --edit)