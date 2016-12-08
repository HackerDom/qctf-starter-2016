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

ssh $user@$IP 'tmux new -s deploy -d'
ssh $user@$IP 'tmux send -t deploy " bash -c \"\
./prepare_local_machine.sh; \
./create_template_container.sh; \
./copy_containers.sh; \
./prepare_webcam.sh; \
./add_iptables_rules.sh; \
rm prepare_local_machine.sh; \
rm create_template_container.sh; \
rm copy_containers.sh; \
rm prepare_webcam.sh; \
reboot\" > deploy_log.txt 2>&1" enter'
