#!/bin/bash

set -xe

modprobe v4l2loopback
chmod 777 /dev/video0
while true; do
	ffmpeg -re -i video.mp4 -f v4l2 /dev/video0
done
