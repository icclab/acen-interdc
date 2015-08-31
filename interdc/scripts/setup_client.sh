#!/bin/bash
# Script for setting up OpenVPN client

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A INPUT -i tun+ -j ACCEPT
iptables -A FORWARD -i tun+ -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o tun+ -j ACCEPT

sudo apt-get update
sudo apt-get install -y openvpn

cp ./static.key /etc/openvpn/

sed -e 's/SERVER_ADDRESS/'$SERVER_ADDRESS'/g' \
    -e 's/SERVER_SUBNET/'$SERVER_SUBNET'/g' \
    -e 's/SERVER_MASK/'$SERVER_MASK'/g' \
    < ./client.conf.template > ./client.conf

cp ./client.conf /etc/openvpn/

mkdir /etc/openvpn/ccd
touch /etc/openvpn/ccd/client

# TO BE CUSTOMIZED
echo 'iroute '$CLIENT_SUBNET' '$CLIENT_MASK >> /etc/openvpn/ccd/client

service openvpn restart
