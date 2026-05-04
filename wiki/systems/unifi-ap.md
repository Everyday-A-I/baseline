---
title: Ubiquiti UniFi AP U6-Lite
category: system
tags: [wifi, ubiquiti, unifi, access-point, wpa3]
systems: [unifi-ap]
last_updated: 2026-04-26
version_notes: "Firmware 7.0.66"
llm_threads: []
---

# Ubiquiti UniFi AP U6-Lite

## Overview

WiFi 6 (802.11ax) access point providing wireless coverage for the homelab. Managed standalone (no UniFi controller) via SSH and local web UI. Broadcasts two SSIDs: `homelab` (WPA3, personal devices) and `homelab-iot` (WPA2, IoT devices including Tapo Hub). PoE powered from tp-link-switch port 8.

## Hardware / Specs

| Field | Value |
|---|---|
| Model | Ubiquiti UniFi AP U6-Lite |
| WiFi | 802.11ax (WiFi 6) dual-band |
| 2.4 GHz | 2×2 MU-MIMO, up to 300 Mbps |
| 5 GHz | 2×2 MU-MIMO, up to 1,200 Mbps |
| Uplink | 1× Gigabit Ethernet (PoE 802.3af/at) |
| Max clients | ~100 (practical: <30) |
| Power draw | 10 W (PoE) |

## Software Stack

- Firmware: 7.0.66 (managed standalone — no UniFi Network Application)
- SSH key: `Homelab/unifi-ap root` in KeePassXC

## Network Position

- **IP**: 192.168.1.6/24 (static DHCP lease via MAC)
- **Connected to**: tp-link-switch port 8 (PoE)
- **DHCP**: clients receive addresses from openwrt-primary (192.168.1.50–199)

### SSID Map

| SSID | Band | Security | Purpose |
|---|---|---|---|
| `homelab` | 2.4 + 5 GHz | WPA3 | Personal devices |
| `homelab-iot` | 2.4 GHz only | WPA2 | IoT devices (Tapo Hub, etc.) |

## Health Baseline

```yaml
health_baseline:
  interfaces: [eth0]
  ssids_up: [homelab, homelab-iot]
  uptime_min_days: 14
  associated_clients_max: 30
openclaw_monitor: true
openclaw_skill: homelab/monitor-unifi-ap
```

## Field Notes

- 2026-02-20: Switched to standalone management after removing UniFi controller (was running on pi4-monitor, consuming 600 MB RAM unnecessarily).
- 2026-04-03: Firmware 7.0.66 applied via SSH `syswrapper.sh upgrade`. No client disruption (clients reconnected within 30s).
- 2026-04-18: 5 GHz band achieving ~850 Mbps throughput at 3m distance. Adequate for all current use cases.

## Related Pages

- `[[tp-link-switch|TP-Link Managed Switch]]`
- `[[tapo-hub|Tapo Hub H100]]`
- `[[../network/topology|Network Topology]]`

## Sources

- [UniFi U6-Lite datasheet](https://techspecs.ui.com/unifi/wifi/u6-lite)
- [UniFi standalone mode](https://help.ui.com/hc/en-us/articles/204909444)
