---
title: TP-Link TL-SG2008P Managed Switch
category: system
tags: [switch, tp-link, managed, poe, vlan]
systems: [tp-link-switch]
last_updated: 2026-04-26
version_notes: "Firmware 3.0.0 Build 20231226"
llm_threads: []
---

# TP-Link TL-SG2008P Managed Switch

## Overview

8-port Gigabit managed PoE+ switch. Central LAN distribution point: every device in the homelab connects here. PoE powers the UniFi AP and the Tapo Hub. Currently running a flat VLAN 1 topology (no VLAN segmentation) — IoT VLAN segmentation is a planned future step.

## Hardware / Specs

| Field | Value |
|---|---|
| Model | TP-Link TL-SG2008P |
| Ports | 8× Gigabit (ports 1–4 PoE+, ports 5–8 non-PoE) |
| PoE budget | 62 W total |
| Management | Web UI (L2+), SNMP v2/v3 |
| Power | 60 W internal PSU |

## Software Stack

- Firmware: 3.0.0 Build 20231226
- Management: Web UI at https://192.168.1.5 (local management, no Omada cloud)
- SNMP: enabled (read-only community `public`, v2c — to be locked down)

## Network Position

- **IP**: 192.168.1.5/24 (static)
- **VLAN**: Single VLAN 1 (untagged, all ports)

### Port Map

| Port | Device | Notes |
|---|---|---|
| 1 | openwrt-primary | Uplink (2.5 GbE via 2.5G→1G adapter) |
| 2 | openwrt-standby | Standby router LAN |
| 3 | proxmox-main | Server uplink |
| 4 | pi4-monitor | Monitoring SBC (PoE powered) |
| 5 | synology-ds923 | NAS trunk (port 5+6 LACP) |
| 6 | synology-ds923 | NAS trunk (port 5+6 LACP) |
| 7 | pi5-services | Services SBC |
| 8 | unifi-ap | AP uplink (PoE powered) |

*Tapo Hub (192.168.1.40) connects via WiFi through unifi-ap.*

## Health Baseline

```yaml
health_baseline:
  interfaces: [all]
  poe_budget_w_max: 55
  uptime_min_days: 30
  snmp_reachable: true
openclaw_monitor: true
openclaw_skill: homelab/monitor-tp-link-switch
```

## Field Notes

- 2026-01-30: Enabled LACP (802.3ad) on ports 5+6 for synology-ds923. Throughput on NFS backup now saturates gigabit.
- 2026-04-12: SNMP community string is still `public` — tracked as a low-priority hardening task. Only pi4-monitor scrapes it.

## Related Pages

- `[[../network/topology|Network Topology]]`
- `[[../network/ip-schema|IP Schema]]`
- `[[unifi-ap|UniFi AP U6-Lite]]`

## Sources

- [TL-SG2008P datasheet](https://www.tp-link.com/uk/business-networking/easy-smart-switch/tl-sg2008p/)
