#!/bin/bash

SRC="/home/simple-web/qctf-starter-2016"
DST="/var/www"

mkdir -p $DST/{badip,clicker,grouping-s,guide}/www
mkdir -p $DST/deploy

cp -R $SRC/badip/* $DST/badip/www
cp -R $SRC/destructive-clicker/* $DST/clicker/www
cp -R $SRC/kurlyandian/* $DST/grouping-s/www
cp -R $SRC/installation-guide/* $DST/guide/www
# cp -R $SRC/dna-encode/* $DST/dna/www # not implemented yet
cp -R $SRC/deploy/* $DST/deploy

cp $SRC/deploy/simple-web/nginx.conf /etc/nginx/nginx.conf
