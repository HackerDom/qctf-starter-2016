#!/bin/bash

SRC="/home/simple-web/qctf-starter-2016"
DST="/var/www"

mkdir -p $DST/{badip,clicker,grouping-s}/www
mkdir -p $DST/deploy

cp -R $SRC/badip/* $DST/badip/www
cp -R $SRC/destructive-clicker/* $DST/clicker/www
cp -R $SRC/kurlyandian/* $DST/grouping-s/www
# cp -R $SRC/dna-encode/* $DST/dna/www
cp -R $SRC/deploy/* $DST/deploy
