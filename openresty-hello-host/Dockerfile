# 2020-06-11 01
FROM openresty/openresty:alpine
MAINTAINER pasi@pashi.net
ADD etc/default.conf /etc/nginx/conf.d/default.conf
RUN echo 'env HOSTNAME;' >> /usr/local/openresty/nginx/conf/nginx.conf
