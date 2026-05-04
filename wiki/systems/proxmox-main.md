---
title: Proxmox VE Main Server
category: system
tags: [proxmox, hypervisor, compute, vm, lxc]
systems: [proxmox-main]
last_updated: 2026-04-26
version_notes: "Proxmox VE 8.2"
llm_threads: []
---

# Proxmox VE Main Server

## Overview

Primary compute node running Proxmox VE. Hosts all production VMs and LXC containers for the homelab. No HA cluster — single node with regular backups to `synology-ds923`. Managed via web UI (https://192.168.1.10:8006) and CLI over SSH.

## Hardware / Specs

| Field | Value |
|---|---|
| Chassis | Mini-ITX in Fractal Node 304 |
| CPU | Intel Core i5-12400 (6C/12T, up to 4.4 GHz) |
| RAM | 64 GB DDR4-3200 ECC (2× 32 GB Crucial) |
| Boot disk | 500 GB Samsung 980 Pro NVMe (VM OS drives) |
| Data disk | 2 TB WD Red SN700 NVMe (VM data, bulk) |
| NIC | 2× Gigabit (Intel I225-V onboard, 1× PCI-e Intel I350) |
| GPU | None (headless) |
| Power | Corsair SF600 Platinum |

## Software Stack

| Package | Version | Purpose |
|---|---|---|
| Proxmox VE | 8.2 | Hypervisor |
| Debian | 12 (Bookworm) | Host OS base |
| ZFS | 2.2 | Boot pool (mirror), VM pool |
| PBS client | 3.0 | Proxmox Backup Server client → synology-ds923 |

### Active VMs / Containers

| ID | Name | Type | vCPU | RAM | IP | Purpose |
|---|---|---|---|---|---|---|
| 100 | pihole-lxc | LXC (priv) | 1 | 512 MB | 192.168.1.22 | Fallback DNS (AdGuard on pi5) |
| 101 | monitoring-lxc | LXC (priv) | 2 | 2 GB | 192.168.1.23 | Prometheus remote write target |
| 200 | win11-gaming | VM | 8 | 16 GB | DHCP | Windows 11 (PCIe passthrough GPU) |
| 201 | dev-ubuntu | VM | 4 | 8 GB | 192.168.1.24 | Dev environment |

## Network Position

- **Management IP**: 192.168.1.10/24 (static, vmbr0 bridge)
- **VM bridge**: vmbr0 (all VMs on LAN segment)
- **Connected to**: tp-link-switch port 3 (tagged VLAN 1)

## Health Baseline

```yaml
health_baseline:
  interfaces: [eno1]
  cpu_usage_pct_max: 80
  ram_usage_pct_max: 90
  zfs_pool_status: ONLINE
  disk_temp_c_max: 65
  uptime_min_days: 14
openclaw_monitor: true
openclaw_skill: homelab/monitor-proxmox-main
```

## Field Notes

- 2026-01-15: Added 32 GB RAM (now 64 GB). dev-ubuntu VM migrated from 4 to 8 GB.
- 2026-03-30: ZFS scrub completed — 0 errors. Schedule: first Saturday of each month via cron.
- 2026-04-20: Proxmox updated to 8.2. Reboot required; LXC containers resumed automatically. VMs started manually.

## Related Pages

- `[[synology-ds923|Synology DS923+ NAS]]`
- `[[../runbooks/proxmox-vm-backup|Proxmox VM Backup Runbook]]`
- `[[../network/ip-schema|IP Schema]]`

## Sources

- [Proxmox VE documentation](https://pve.proxmox.com/pve-docs/)
- [ZFS on Proxmox](https://pve.proxmox.com/wiki/ZFS_on_Linux)
