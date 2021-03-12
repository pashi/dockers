FROM alpine:3
MAINTAINER pasi@pashi.net
ADD requirements.txt /
RUN apk add --update py3-pip py3-cffi py3-cryptography; pip install -r requirements.txt ; mkdir -p /app
ADD feedreader.py /
WORKDIR /app
VOLUME ["/app"]
CMD ["/usr/bin/python3", "/feedreader.py"]
