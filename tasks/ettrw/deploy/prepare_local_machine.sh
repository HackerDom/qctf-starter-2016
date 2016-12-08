#!/bin/bash

BLOCK_STORAGE=true
USE_SWAP=false
if [[ $BLOCK_STORAGE == false ]]; then
	BTRFS_SIZE="120G"
fi
if $USE_SWAP; then
	SWAP_SIZE_GB=16
fi

set -xe

# apt-get update
echo "Updating apt"
apt-get update

# Locales
echo "Configuring locales"
locale-gen ru_RU.UTF-8
dpkg-reconfigure --frontend=noninteractive locales

# Btrfs
echo "Preparing btrfs"

apt-get install -y btrfs-tools
mkdir -p /var/lib/lxc

if $BLOCK_STORAGE; then
	device="/dev/disk/by-id/"`ls /dev/disk/by-id | grep volume`

	echo "Using device $device for btrfs"

	mkfs.btrfs $device
	mount $device /var/lib/lxc

	echo "$device	/var/lib/lxc	btrfs	compress-force=zlib	0 0" >> /etc/fstab
else
	truncate -s $BTRFS_SIZE /var/lib/lxc.img
	losetup /dev/loop0 /var/lib/lxc.img

	mkfs.btrfs /dev/loop0
	mount /dev/loop0 /var/lib/lxc

	echo "/var/lib/lxc.img	/var/lib/lxc	btrfs	loop,compress-force=zlib	0 0" >> /etc/fstab
fi
# Preparing swap
if $USE_SWAP; then
	echo "Preparing swap"

	swap_file="/swap.img"
	truncate -s $SWAP_SIZE_GB"G" $swap_file
	dd if=/dev/zero of=$swap_file bs=1024 count=$(($SWAP_SIZE_GB * 1048576))
	chmod 0600 $swap_file
	mkswap $swap_file
	swapon $swap_file
	echo "$swap_file          swap            swap    defaults        0 0" >> /etc/fstab
fi
# Limits
echo "Updating limits"

echo '* hard nofile 65536' >> /etc/security/limits.conf
echo '* soft nofile 65536' >> /etc/security/limits.conf
echo 'root hard nofile 65536' >> /etc/security/limits.conf
echo 'root soft nofile 65536' >> /etc/security/limits.conf

echo "fs.inotify.max_user_watches = 1048576" >> /etc/sysctl.conf
echo "fs.inotify.max_user_instances = 262144" >> /etc/sysctl.conf
echo "fs.file-max = 262144" >> /etc/sysctl.conf
echo "vm.drop_caches = 3" >> /etc/sysctl.conf
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf

sysctl -p

# Install telegraf
echo "Installing telegraf"

curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

apt-get update
apt-get install -y telegraf

# telegraf-lxc-stats {
apt-get install -y golang-go
apt-get install -y lxc-dev
git clone https://github.com/r0bj/telegraf-lxc-stats.git
pushd telegraf-lxc-stats
export GOPATH=`pwd`
export GOBIN=`pwd`
go get
go build
cp telegraf-lxc-stats /usr/local/bin
popd
rm -rf telegraf-lxc-stats
# }

mv /etc/telegraf/telegraf.conf{,.default}
mv telegraf.conf /etc/telegraf/
mv telegraf_sudoer /etc/sudoers.d/telegraf
chmod 644 /etc/sudoers.d/telegraf

systemctl restart telegraf

#Installing lxc
echo "Installing lxc"
apt-get install -y lxc

# Persiatent iptables
echo "Installing iptables-persistent"
DEBIAN_FRONTEND=noninteractive apt-get install -yq iptables-persistent
