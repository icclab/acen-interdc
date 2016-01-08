# ACEN NFV USE CASE - Inter-DC connectivity

Simple OpenVPN client-server setup providing inter-datacenter connectivity.

Please set environment variables in the settings file accordingly before running scripts.

Example network schema :

           DC 1                      DC 2

    ------------------        -------------------
    |OpenVPN Server   |       |OpenVPN Client   |
    |tun0: 10.8.0.1   |=======|tun0: 10.8.0.2   |
    |eth0: 10.0.0.2/24|       |eth0: 10.0.1.3/24|
    -------------------       -------------------
             |                         |
    -------------------       -------------------
    |VM 1             |       |VM 2             |
    |eth0: 10.0.0.8/24|       |eth0: 10.0.1.7/24|
    -------------------       -------------------

## Heat Orchestration Templates

More information on multi-region InterDC Heat orchestration templates can be found [here](https://github.com/icclab/acen-interdc/blob/master/Heat/README.md).

## Acknowledgment
This work was made possible by the [KTI ACEN project](http://blog.zhaw.ch/icclab/acen-begins/) in collaboration with [Citrix](https://www.citrix.com/) and [Exoscale](https://www.exoscale.ch/).
