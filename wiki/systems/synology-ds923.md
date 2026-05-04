---
title: Synology DS923+ NAS
category: system
tags: [nas, synology, storage, backup, smb, nfs]
systems: [synology-ds923]
last_updated: 2026-04-26
version_notes: "DSM 7.2.1-69057 Update 5"
llm_threads: []
---

# Synology DS923+ NAS

## Overview

Primary network storage for the homelab. Serves SMB shares for general storage and NFS shares for VM backup targets. Runs Synology Photos and Synology Drive for family file sync. Acts as the Proxmox Backup Server (PBS) NFS target for VM snapshots.

## Hardware / Specs

| Field | Value |
|---|---|
| Model | Synology DS923+ |
| CPU | AMD Ryzen R1600 (2C/4T, up to 3.1 GHz) |
| RAM | 4 GB DDR4 ECC (expandable to 32 GB) |
| Drives | 4× 4 TB WD Red Plus (SHR-2, ~8 TB usable) |
| NIC | 2× Gigabit (port trunk to tp-link-switch) |
| M.2 | 2× NVMe slots (read cache: 2× 500 GB WD SN570) |
| Power | ~35 W active, ~8 W sleep |

## Software Stack

| Package | Purpose |
|---|---|
| DSM 7.2.1 | Base OS |
| Synology Drive | File sync (family devices) |
| Synology Photos | Photo library (replacing Google Photos) |
| Hyper Backup | Off-site backup → Backblaze B2 |
| NFS | VM backup target for proxmox-main |
| SMB | General homelab shares |

### Share Layout

| Share | Protocol | Used By | Path |
|---|---|---|---|
| `backups` | NFS | proxmox-main (PBS target) | /volume1/backups |
| `media` | SMB | All LAN clients | /volume1/media |
| `documents` | SMB | Personal devices | /volume1/documents |
| `photos` | Synology Photos | Drive app | /volume1/photo |

## Network Position

- **IP**: 192.168.1.30/24 (static)
- **Connected to**: tp-link-switch ports 5+6 (802.3ad LACP trunk, 2 Gbps bonded)
- **NFS exports**: `/volume1/backups` → 192.168.1.10 (proxmox-main), rw, no_root_squash

## Health Baseline

```yaml
health_baseline:
  interfaces: [bond0]
  volume_status: normal
  disk_health: good
  disk_temp_c_max: 50
  shr_degraded: false
  smb_shares_reachable: true
openclaw_monitor: true
openclaw_skill: homelab/monitor-synology-ds923
```

## Field Notes

- 2026-01-20: Added NVMe read cache (2× 500 GB). Sequential read improved ~40% for SMB workloads.
- 2026-03-05: Drive 3 (WD Red 4 TB) SMART warning (reallocated sectors: 8). Replaced under warranty. SHR-2 rebuilt in 18 hours with no degradation.
- 2026-04-15: Hyper Backup → Backblaze B2 confirmed: weekly full, daily incremental. Last verified restore: 2026-03-01.

## Related Pages

- `[[proxmox-main|Proxmox VE Main Server]]`
- `[[../runbooks/proxmox-vm-backup|Proxmox VM Backup Runbook]]`
- `[[../network/ip-schema|IP Schema]]`

## Sources

- [Synology DS923+ product page](https://www.synology.com/products/DS923+)
- [DSM release notes](https://www.synology.com/releaseNote/DSMmanager)
