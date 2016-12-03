#!/bin/bash

SRC="/root/qctf-starter-2016"
DST="/var/www"

mkdir -p $DST/grouping-s/www

cp -R $SRC/kurlyandian/destroy $DST/grouping-s/www
cp -R $SRC/kurlyandian/explore $DST/grouping-s/www
cp -R $SRC/kurlyandian/learn $DST/grouping-s/www

SRC="$SRC/deploy/grouping-s-s"

cp $SRC/nginx.conf /etc/nginx/nginx.conf
