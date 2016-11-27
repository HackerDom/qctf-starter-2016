#!/bin/bash

SRC="/root/qctf-starter-2016"
DST="/var/www"

mkdir -p $DST/grouping-s/www

cp -R $SRC/kurlyandian/* $DST/grouping-s/www

SRC="$SRC/deploy/simple-web"

cp $SRC/nginx.conf /etc/nginx/nginx.conf
