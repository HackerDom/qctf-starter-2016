#!/bin/bash

CONTAINER_NAME="template_container"
USERNAME="user"

# dhcp
sed -i 's/LXC_NETMASK="255.255.255.0"/LXC_NETMASK="255.255.0.0"/g' /etc/default/lxc-net
sed -i 's/LXC_NETWORK="10.0.3.0\/24"/LXC_NETWORK="10.0.3.0\/16"/g' /etc/default/lxc-net
sed -i 's/LXC_DHCP_RANGE="10.0.3.2,10.0.3.254"/LXC_DHCP_RANGE="10.0.3.2,10.0.8.254"/g' /etc/default/lxc-net
sed -i 's/LXC_DHCP_MAX="253"/LXC_DHCP_MAX="512"/g' /etc/default/lxc-net
sed -i 's/#LXC_DHCP_CONFILE=\/etc\/lxc\/dnsmasq.conf/LXC_DHCP_CONFILE=\/etc\/lxc\/dnsmasq.conf/g' /etc/default/lxc-net
echo "dhcp-hostsfile=/etc/lxc/dnsmasq-hosts.conf" >> /etc/lxc/dnsmasq.conf

# Template container

lxc-create -B btrfs -t ubuntu -n $CONTAINER_NAME -- --user $USERNAME

mv team-machine.common.conf /usr/share/lxc/config/

echo "# Limits configuration" >> /var/lib/lxc/$CONTAINER_NAME/config
echo "lxc.include = /usr/share/lxc/config/team-machine.common.conf" >> /var/lib/lxc/$CONTAINER_NAME/config

user_home_dir=/var/lib/lxc/$CONTAINER_NAME/rootfs/home/procruster
mkdir -p $user_home_dir
cp webcam/webcam_2016_06_14_231417.jpg $user_home_dir

echo "PROMPT_COMMAND=\"history -a;\$PROMPT_COMMAND\"" >> /var/lib/lxc/$CONTAINER_NAME/rootfs/home/user/.bashrc

lxc-start -n $CONTAINER_NAME

lxc-attach -n $CONTAINER_NAME -- bash -c "apt-get update"
lxc-attach -n $CONTAINER_NAME -- bash -c "apt-get install -y streamer vlc ffmpeg mplayer mencoder"

lxc-stop -n $CONTAINER_NAME
