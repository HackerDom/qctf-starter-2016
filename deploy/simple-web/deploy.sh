#!/bin/bash

SRC="/home/simple-web/qctf-starter-2016"
DST="/var/www"

mkdir -p $DST/{badip,clicker,grouping-s,guide}/www

cp -R $SRC/badip/* $DST/badip/www
cp -R $SRC/destructive-clicker/* $DST/clicker/www
cp -R $SRC/kurlyandian/* $DST/grouping-s/www
cp -R $SRC/installation-guide/* $DST/guide/www

mkdir -p $DST/deploy

SRC="$SRC/deploy/simple-web"
DST="$DST/deploy/simple-web"

cp $SRC/docker-compose.yml $DST/docker-compose.yml
cp $SRC/nginx.conf /etc/nginx/nginx.conf
cp $SRC/compose-simple-web.service \
  /etc/systemd/system/compose-simple-web.service
