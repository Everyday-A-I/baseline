---
title: OpenWrt Standby Router
category: system
tags: [router, openwrt, standby, lte, failover]
systems: [openwrt-standby]
last_updated: 2026-04-26
version_notes: "OpenWrt 23.05.3"
llm_threads: []
---

# OpenWrt Standby Router

## Overview

Secondary/standby router that sits idle during normal operation (Scheme A). Provides WAN continuity in two failure modes: as a secondary WAN path via the primary router (Scheme B) or as a full LAN gateway replacement if the primary router fails (Scheme C). Runs a Quectel EC25 LTE modem on USB for its own WAN. DHCP server is disabled in Scheme A.

## Hardware / Specs

| Field | Value |
|---|---|
| Model | Raspberry Pi 4B (4 GB RAM) with OpenWrt |
| CPU | Broadcom BCM2711, 4× Cortex-A72 @ 1.5 GHz |
| RAM | 4 GB LPDDR4 |
| Storage | 32 GB microSD (SanDisk Endurance) |
| LAN | 1× Gigabit Ethernet (to tp-link-switch, port 2) |
| USB | 1× USB 3.0 (quectel-ec25 shared modem via USB hub) |
| Power | 5 V USB-C, ~5 W typical |

## Software Stack

| Package | Purpose |
|---|---|
| OpenWrt 23.05.3 | Base OS |
| luci | Web UI |
| kmod-usb-net-qmi-wwan | Quectel EC25 modem driver |
| uqmi | QMI modem control utility |
| nftables | Firewall |

## Network Position

- **LAN IP**: 192.168.1.2/24 (static, always reachable from LAN)
- **WAN (LTE)**: QMI via Quectel EC25 — connected but idle in Scheme A
- **DHCP server**: Disabled in Scheme A; enabled with range 192.168.1.50–199 in Scheme C
- **Default gateway published**: None in Scheme A; 192.168.1.2 in Scheme C

## Health Baseline

```yaml
health_baseline:
  interfaces: [eth0, wwan0]
  lte_connected: true
  lte_rssi_dbm_min: -90
  reachable_from_lan: true
openclaw_monitor: true
openclaw_skill: homelab/monitor-openwrt-standby
```

## Field Notes

- 2026-03-12: During fibre outage, standby LTE was up throughout. Primary router used Scheme A failover via mwan3 — standby was not promoted.
- 2026-04-15: Tested Scheme B manually (lab window). Promoted standby WAN via DHCP option 3 change on primary. Clients recovered within 90s. See `[[../runbooks/scheme-b-standby-wan|Scheme B runbook]]`.

## Related Pages

- `[[../network/routing-schemes|Routing Schemes]]`
- `[[../meta/routing-state|Current Routing State]]`
- `[[openwrt-primary|OpenWrt Primary Router]]`
- `[[quectel-ec25|Quectel EC25 LTE Modem]]`

## Sources

- [OpenWrt on Raspberry Pi](https://openwrt.org/toh/raspberry_pi_foundation/raspberry_pi)
