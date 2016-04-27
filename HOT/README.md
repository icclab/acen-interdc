# Heat orchestration templates (HOT) for multi-region L3 Inter-DC connectivity

## CloudStack <-> CloudStack

Orchestrates OpenVPN Client and OpenVPN Server machines and establishes a VPN connection between two remote isolated CloudStack networks.

```
cs-cs.yaml
```

## CloudStack <-> OpenStack

Orchestrates OpenVPN Client (OpenStack) and OpenVPN Server (CloudStack) machines and establishes a VPN connection between CloudStack and OpenStack networks.

```
cs-os.yaml
```

## OpenStack <-> CloudStack

Orchestrates OpenVPN Client (CloudStack) and OpenVPN Server (OpenStack) machines and establishes a VPN connection between CloudStack and OpenStack networks.

```
os-cs.yaml
```
