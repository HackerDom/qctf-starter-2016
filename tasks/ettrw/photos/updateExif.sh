#!/bin/bash

exiftool -all= $1
exiftool $1 -Model="HD Webcam" -Make="Logitech" -Date="2016:06:14 23:14:17+05:00" -XMP=""
touch -t 201606142314 $1
rm $1"_original"
