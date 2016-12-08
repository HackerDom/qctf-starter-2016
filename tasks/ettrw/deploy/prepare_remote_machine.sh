#!/bin/bash

if [[ $1 == "" ]]; then
	echo "Usage:"
	echo $0" IP"
	exit
fi

set -xe

user="root"
IP=$1
remoteWorkDir="/root"

scp -o "StrictHostKeyChecking no" telegraf.conf telegraf_sudoer prepare_local_machine.sh create_template_container.sh copy_containers.sh team-machine.common.conf add_iptables_rules.sh prepare_webcam.sh generatePasswords.py $user@$IP:$remoteWorkDir

ssh $user@$IP "mkdir webcam"
scp -r ../webcam/deploy/* $user@$IP:$remoteWorkDir/webcam
scp ../video.mp4 ../photos/webcam_2016_06_14_231417.jpg $user@$IP:$remoteWorkDir/webcam

ssh $user@$IP ./prepare_local_machine.sh
ssh $user@$IP ./create_template_container.sh
ssh $user@$IP ./copy_containers.sh
ssh $user@$IP ./prepare_webcam.sh
ssh $user@$IP ./add_iptables_rules.sh

ssh $user@$IP "rm prepare_local_machine.sh"
ssh $user@$IP "rm create_template_container.sh"
ssh $user@$IP "rm copy_containers.sh"
ssh $user@$IP "rm prepare_webcam.sh"
ssh $user@$IP "reboot"
