---
title: Tapo Hub H100
category: system
tags: [iot, tapo, smart-home, hub, zigbee]
systems: [tapo-hub]
last_updated: 2026-04-26
version_notes: "Hub firmware 1.4.2"
llm_threads: []
---

# Tapo Hub H100

## Overview

TP-Link Tapo smart home hub. Bridges Tapo sensors and devices (door/window sensors, temperature sensors, motion sensors) to the LAN. Home Assistant integrates via the Tapo cloud API. Future goal is local-only control (Home Assistant local polling or Matter bridging). Currently requires cloud for full function — flagged as a dependency to resolve.

## Hardware / Specs

| Field | Value |
|---|---|
| Model | TP-Link Tapo Hub H100 |
| Connectivity | 2.4 GHz WiFi (802.11 b/g/n), 868/915 MHz (Tapo RF) |
| Power | 100–240 V AC (wall plug) |
| Devices supported | Up to 64 Tapo sensors |

## Software Stack

- Tapo firmware 1.4.2
- Home Assistant integration: Tapo cloud API via `hatapon` custom component (HACS)

### Connected Devices

| Device | Model | Room | Sensor Type |
|---|---|---|---|
| Front door | Tapo T110 | Hallway | Door/window open/close |
| Back door | Tapo T110 | Kitchen | Door/window open/close |
| Server room | Tapo T315 | Utility room | Temp + humidity |
| Living room | Tapo T315 | Living room | Temp + humidity |
| Motion 1 | Tapo T100 | Hallway | Motion |

## Network Position

- **IP**: 192.168.1.40/24 (static DHCP lease via MAC)
- **Connected via**: WiFi (unifi-ap, 2.4 GHz SSID `homelab-iot`)
- **Cloud dependency**: Requires Tapo cloud for firmware updates and full API access

## Health Baseline

```yaml
health_baseline:
  reachable_from_lan: true
  cloud_connection: true
  device_count_min: 5
openclaw_monitor: true
openclaw_skill: homelab/monitor-tapo-hub
```

## Field Notes

- 2026-03-01: Server room temp sensor triggered HA automation at 32°C — Telegram alert sent, fan confirmed running normally (transient spike during Proxmox scrub).
- 2026-04-01: Investigated local Matter bridging. H100 does not currently expose Matter locally without cloud. Tracked as open question.

## Related Pages

- `[[pi4-monitor|Raspberry Pi 4 — Monitoring]]`
- `[[unifi-ap|UniFi AP U6-Lite]]`
- `[[../network/ip-schema|IP Schema]]`

## Sources

- [Tapo H100 product page](https://www.tapo.com/uk/product/smart-hub/tapo-h100/)
- [Home Assistant Tapo integration](https://github.com/petretiandrea/home-assistant-tapo-p100)
