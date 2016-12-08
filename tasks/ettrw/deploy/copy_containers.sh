#!/bin/bash

set -xe

AMOUNT_OF_COPIES=400
TEMPLATE_CONTAINER="template_container"
TARGET_NAME_PREFIX="team-"
USERNAME="user"

if [[ `lxc-info -n template_container | grep -o STOPPED` != "STOPPED" ]]; then
	lxc-stop -n $TEMPLATE_CONTAINER
fi

chmod +x /var/lib/lxc

for i in `seq $AMOUNT_OF_COPIES`;
do
	uid=$(($i * 100000))
	usermod --add-subuids $uid-$(($uid + 65536)) root
	usermod --add-subgids $uid-$(($uid + 65536)) root
	name=$TARGET_NAME_PREFIX$i
	lxc-copy -n $TEMPLATE_CONTAINER -N $name
	chown -R $uid:$uid /var/lib/lxc/$name
	echo "# Users" >> /var/lib/lxc/$name/config
	echo "lxc.id_map = u 0 $uid 65536" >> /var/lib/lxc/$name/config
	echo "lxc.id_map = g 0 $uid 65536" >> /var/lib/lxc/$name/config
	echo "$uid hard nproc 256" >> /etc/security/limits.conf
	echo "$uid soft nproc 256" >> /etc/security/limits.conf
	zero_i=$(($i-1))
	ip="10.0."$((4 + $zero_i / 255)).$(($zero_i % 255 + 1))
	echo "$name,$ip" >> /etc/lxc/dnsmasq-hosts.conf
done;

service lxc-net restart

lxc-autostart

./generatePasswords.py $AMOUNT_OF_COPIES
rm generatePasswords.py

for i in `seq $AMOUNT_OF_COPIES`;
do
	pass=`grep -Po "(?<=^$i - )(.*)" passwords.txt`
	lxc-attach -n $TARGET_NAME_PREFIX$i -- bash -c "echo "$USERNAME:$pass" | chpasswd"
	lxc-attach -n $TARGET_NAME_PREFIX$i -- bash -c "chmod 4755 /usr/bin/sudo"
	lxc-attach -n $TARGET_NAME_PREFIX$i -- bash -c "chown -R user:user /home/user"
done;
