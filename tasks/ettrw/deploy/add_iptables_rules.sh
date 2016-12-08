#!/bin/bash

set -xe

NAME_PREFIX="team"
START_PORT=50000

IFS=$'\n'
for line in `lxc-ls --running --filter $NAME_PREFIX.* -f -F NAME,IPV4 | tail -n +2`;
do
	echo $line
	name=`echo $line | grep -Po "^\S+"`
	id=`echo $name | grep -Po "(\d*)$"`
	ip=`echo $line | grep -Po "(\d*\.\d*\.\d*\.\d*)"`
	port=$(($START_PORT + $id))
	echo "$ip"
	iptables -t nat -A PREROUTING -p tcp --dport $port -j DNAT --to-destination $ip:22 -m comment --comment "$name"
done

iptables -t nat -A POSTROUTING -j MASQUERADE

iptables-save > /etc/iptables/rules.v4
