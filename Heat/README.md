# Heat orchestration templates for multi-region Inter-DC connectivity

## CloudStack <-> CloudStack

Orchestrates OpenVPN Client and OpenVPN Server machines and establishes a VPN connection between two remote isolated CloudStack networks.

```
cs-os.yaml
```

## CloudStack <-> OpenStack

Orchestrates OpenVPN Client (OpenStack) and OpenVPN Server (CloudStack) machines and establishes a VPN connection between CloudStack and OpenStack networks.

```
cs-cs.yaml
```
