#!/bin/bash
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
echo "$sshkey" >> ~/.ssh/authorized_keys
touch /tmp/vars
echo SERVER_ADDRESS=$vpn_server_addr >> /tmp/vars
echo SERVER_SUBNET=$server_subnet >> /tmp/vars
echo SERVER_MASK=$server_mask >> /tmp/vars
echo CLIENT_SUBNET=$client_subnet >> /tmp/vars
echo CLIENT_MASK=$client_mask >> /tmp/vars
wget https://github.com/icclab/acen-interdc/archive/master.tar.gz -O - | tar -xz --directory=/tmp/
chmod +x /tmp/acen-interdc-master/setup_client.sh
/tmp/acen-interdc-master/setup_client.sh
