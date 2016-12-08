#!/bin/bash

set -xe

apt-get install -y linux-generic
apt-get install -y v4l2loopback-dkms
apt-get install -y gstreamer1.0
apt-get install -y ffmpeg

mv webcam/WebcamFeed.service /etc/systemd/system
systemctl daemon-reload
systemctl enable WebcamFeed
systemctl start WebcamFeed
