---
title: Raspberry Pi 5 — Services
category: system
tags: [raspberry-pi, dns, adguard, zerotier, nginx, services]
systems: [pi5-services]
last_updated: 2026-04-26
version_notes: "Raspberry Pi OS Bookworm 2024-11-19"
llm_threads: []
---

# Raspberry Pi 5 — Services

## Overview

Shared services node: LAN-wide DNS with ad blocking (AdGuard Home), ZeroTier controller for the homelab overlay network, and Nginx reverse proxy for internal HTTPS access to services. Acts as the primary DNS server for all LAN clients (configured via DHCP option 6 on openwrt-primary).

## Hardware / Specs

| Field | Value |
|---|---|
| Model | Raspberry Pi 5 (8 GB) |
| CPU | Broadcom BCM2712, 4× Cortex-A76 @ 2.4 GHz |
| RAM | 8 GB LPDDR4X |
| Storage | 128 GB Samsung 990 Pro NVMe (via PCIe HAT) |
| LAN | 1× Gigabit Ethernet |
| Power | Official Pi 5 27W USB-C PSU |

## Software Stack

| Service | Port | Purpose |
|---|---|---|
| AdGuard Home | 53 (DNS), 3000 (UI) | LAN-wide DNS + ad blocking |
| ZeroTier One | 9993/UDP | Overlay network node + controller |
| Nginx | 443 (HTTPS) | Reverse proxy for internal services |
| fail2ban | — | SSH and Nginx brute-force protection |
| node_exporter | 9100 | Prometheus metrics |

### Nginx Upstream Map

| Hostname | Upstream | Service |
|---|---|---|
| `ha.home.arpa` | 192.168.1.20:8123 | Home Assistant |
| `grafana.home.arpa` | 192.168.1.20:3000 | Grafana |
| `proxmox.home.arpa` | 192.168.1.10:8006 | Proxmox web UI |
| `nas.home.arpa` | 192.168.1.30:5000 | Synology DSM |

## Network Position

- **IP**: 192.168.1.21/24 (static)
- **Connected to**: tp-link-switch port 7
- **DNS role**: primary DNS for all LAN clients (DHCP option 6)
- **ZeroTier network**: `1d71939404b3f2b1` (see `[[../network/zerotier|ZeroTier]]`)

## Health Baseline

```yaml
health_baseline:
  interfaces: [eth0]
  services_expected_up: [AdGuardHome, zerotier-one, nginx, fail2ban]
  dns_response_ms_max: 50
  adguard_block_rate_pct_min: 15
  uptime_min_days: 14
openclaw_monitor: true
openclaw_skill: homelab/monitor-pi5-services
```

## Field Notes

- 2026-02-14: Migrated from Pi-hole to AdGuard Home. Block rate improved from 18% to 24%. HTTPS filtering enabled.
- 2026-03-18: Added NVMe HAT. AdGuard query database moved to NVMe; write latency dropped from 8ms to 0.4ms.
- 2026-04-08: Nginx certs renewed via Certbot (Let's Encrypt, DNS challenge via Cloudflare API). 90-day rotation automated via systemd timer.

## Related Pages

- `[[../network/zerotier|ZeroTier]]`
- `[[../network/dns|DNS]]`
- `[[pi4-monitor|Raspberry Pi 4 — Monitoring]]`
- `[[../network/ip-schema|IP Schema]]`

## Sources

- [AdGuard Home docs](https://github.com/AdguardTeam/AdGuardHome/wiki)
- [ZeroTier docs](https://docs.zerotier.com)
