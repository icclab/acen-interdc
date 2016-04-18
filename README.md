# ACEN - NFV USE CASE 1 (UC1) - Inter-DC connectivity

Simple OpenVPN client-server setup providing inter-datacenter connectivity.

Please set environment variables in the settings file accordingly before running scripts.

Example network schema :

    +---------------------------------+         +----------------------------------+
    | DC 1                            |         | DC 2                             |
    +---------------------------------+         +----------------------------------+
    |                                             | 
    |  +--------------------------------+         |  +-------------------------------+
    |--| 10.0.0.0/24 NETWORK            |         |--| 10.0.1.0/24 NETWORK           |
       +--------------------------------+            +-------------------------------+
       |                                             |
       |  +--------------------------------+         |  +-------------------------------+
       |  |Default GW (Router)             |         |  |Default Gateway (Router)       |
       |  |interfaces:                     |         |  |interfaces:                    |
       |--|  eth0: 10.0.0.1/24             |         |--|  eth0: 10.0.1.1/24            |
       |  |routes:                         |         |  |routes:                        |
       |  |   0.0.0.0/0 -> x.x.x.x(eth0)   |         |  |  0.0.0.0/0 -> x.x.x.x(eth0)   |
       |  |   10.0.1.0/24 -> 10.0.0.3(eth0)|         |  |  10.0.0.0/24 -> 10.0.1.3(eth0)|
       |  +--------------------------------+         |  +-------------------------------+
       |                                             |
       |  +--------------------------------+         |  +-------------------------------+
       |  |OpenVPN Server (VM)             |         |  |OpenVPN Client (VM)            |
       |  |interfaces:                     |         |  |interfaces:                    |
       |  |  tun0: 10.8.0.1/32             |============|  tun0: 10.8.0.2/32            |
       |--|  eth0: 10.0.0.3/24             |         |--|  eth0: 10.0.1.3/24            |
       |  |routes:                         |         |  |routes:                        |
       |  |   0.0.0.0/0 -> 10.0.0.1(eth0)  |         |  |  0.0.0.0/0 -> 10.0.1.1(eth0)  |
       |  |   10.8.0.2/32 -> 0.0.0.0(tun0) |         |  |  10.8.0.1/32 -> 0.0.0.0(tun0) |
       |  |   10.0.0.0/24 -> 0.0.0.0(eth0) |         |  |  10.0.1.0/24 -> 0.0.0.0(eth0) |
       |  |   10.0.1.0/24 -> 10.8.0.2(tun0)|         |  |  10.0.0.0/24 -> 10.8.0.1(tun0)|
       |  +--------------------------------+         |  +-------------------------------+
       |                                             |
       |  +--------------------------------+         |  +-------------------------------+
       |  |VM 1                            |         |  |VM 2                           |
       |  |interfaces:                     |         |  |interfaces:                    |
       |--|  eth0: 10.0.0.8/24             |         |--|  eth0: 10.0.1.7/24            |
          |routes:                         |            |routes:                        |
          |  0.0.0.0/0 -> 10.0.0.1(eth0)   |            |  0.0.0.0/24 -> 10.0.1.1(eth0) |
          |  10.0.0.0/24 -> 0.0.0.0(eth0)  |            |  10.0.1.0/24 -> 0.0.0.0(eth0) |
          +--------------------------------+            +-------------------------------+

## Heat Orchestration Templates

More information on multi-region InterDC Heat orchestration templates can be found [here](./Heat/README.md).

## Acknowledgment
This work was made possible by the [KTI ACEN project](http://blog.zhaw.ch/icclab/acen-begins/) in collaboration with [Citrix](https://www.citrix.com/) and [Exoscale](https://www.exoscale.ch/).
