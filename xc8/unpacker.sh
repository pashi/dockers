#!/bin/sh

mkdir -p /opt/packs
ls -lr /downloads
cd /downloads/packs
for f in *.zip
do
unzip $f -d /opt/packs/$(basename $f|sed 's#Microship##g'|sed 's#.zip##g')
done
