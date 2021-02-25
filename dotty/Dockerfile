FROM alpine:3
MAINTAINER pasi@pashi.net
RUN apk add --update graphviz py3-flask py3-graphviz ttf-dejavu
EXPOSE 5000
ADD app /app
CMD ["/usr/bin/python3", "/app/app.py"]
