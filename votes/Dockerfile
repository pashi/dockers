FROM alpine:3
MAINTAINER pasi@pashi.net
RUN apk add --update py3-flask
ADD app.py /
ADD templates /
WORKDIR /app
VOLUME ["/app/data"]
CMD ["/usr/bin/python3", "/app.py"]
