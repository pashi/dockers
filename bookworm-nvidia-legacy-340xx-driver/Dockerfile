FROM docker.io/library/debian:bookworm
MAINTAINER pasi@pashi.net

ARG DEBIAN_FRONTEND=noninteractive
# build tools
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install build-essential fakeroot devscripts debhelper-compat m4 libgl-dev libgtk2.0-dev libjansson-dev libvdpau-dev libxext-dev libxv-dev libxxf86vm-dev pkg-config xserver-xorg-dev debhelper dh-dkms patchelf po-debconf quilt linux-headers-amd64 libsystemd-dev

# debian sid for some sources
RUN echo deb-src http://ftp.fi.debian.org/debian unstable main non-free contrib > /etc/apt/sources.list.d/sid.list
RUN apt-get -y update
RUN mkdir -p /build/nvidia-settings && cd /build/nvidia-settings && apt-get -y source nvidia-settings-legacy-340xx
RUN mkdir -p /build/nvidia340 && cd /build/nvidia340 && apt-get -y source nvidia-legacy-340xx-driver
RUN mkdir -p /build/nvidia-support && cd /build/nvidia-support && apt-get -y source nvidia-support
RUN rm -f /etc/apt/sources.list.d/sid.list

RUN apt-get -y update
RUN cd /build/nvidia-settings/nvidia-settings-legacy-340xx-* && ls -la && debuild -b -uc -us
RUN cd /build/nvidia340/nvidia-graphics-drivers-legacy-340xx-* && ls -la && debuild -b -uc -us

RUN echo 'deb http://deb.debian.org/debian bookworm-backports main' > /etc/apt/sources.list.d/bookworm-backports.list
RUN apt-get -y update && apt-get -y install -t bookworm-backports systemd-dev
RUN cd /build/nvidia-support/nvidia-support-20240109+1 && ls -la && debuild -b -uc -us

RUN mkdir -p /target/non-free/binary-amd64 /target/pool/ /target/dists/bookworm/non-free/binary-amd64 && cp /build/*/*deb /target/pool/ && cd /target/ && dpkg-scanpackages --arch amd64 pool/ > dists/bookworm/non-free/binary-amd64/Packages && cat dists/bookworm/non-free/binary-amd64/Packages|gzip -9 >dists/bookworm/non-free/binary-amd64/Packages.gz
COPY generate-release.sh /target
RUN cd /target/dists/bookworm && sh /target/generate-release.sh > Release


FROM docker.io/library/nginx:mainline-alpine
COPY --from=0 /target /usr/share/nginx/html/
