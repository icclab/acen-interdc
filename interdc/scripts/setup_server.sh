#!/bin/bash
# Script for setting up OpenVPN server
source ./settings

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A INPUT -i tun+ -j ACCEPT
iptables -A FORWARD -i tun+ -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o tun+ -j ACCEPT

sudo apt-get update
sudo apt-get install -y openvpn

cp ./static.key /etc/openvpn/

# Customize server config template
sed -e 's/SERVER_SUBNET/'$SERVER_SUBNET'/g' \
    -e 's/SERVER_MASK/'$SERVER_MASK'/g' \
    -e 's/CLIENT_SUBNET/'$CLIENT_SUBNET'/g' \
    -e 's/CLIENT_MASK/'$CLIENT_MASK'/g' \
    < ./server.conf.template > ./server.conf

cp ./server.conf /etc/openvpn/

service openvpn restart
