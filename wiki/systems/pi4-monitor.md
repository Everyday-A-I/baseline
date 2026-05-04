---
title: Raspberry Pi 4 — Monitoring
category: system
tags: [raspberry-pi, monitoring, home-assistant, grafana, prometheus]
systems: [pi4-monitor]
last_updated: 2026-04-26
version_notes: "Home Assistant OS 12.3"
llm_threads: []
---

# Raspberry Pi 4 — Monitoring

## Overview

Dedicated monitoring SBC running Home Assistant OS. Acts as the primary observability node for the homelab: Home Assistant for smart home and device state, Grafana for dashboards, and Prometheus for metrics collection (scraped from node_exporter on all Linux hosts, and from OpenWrt via prometheus-node-exporter-lua).

This is the SBC that OpenClaw is primarily hosted on and communicates through.

## Hardware / Specs

| Field | Value |
|---|---|
| Model | Raspberry Pi 4B (8 GB RAM) |
| CPU | Broadcom BCM2711, 4× Cortex-A72 @ 1.8 GHz (OC) |
| RAM | 8 GB LPDDR4 |
| Storage | 256 GB Samsung USB SSD (boot + HA data) |
| LAN | 1× Gigabit Ethernet |
| Power | Official Pi 4 27W USB-C PSU |

## Software Stack

| Service | Port | Purpose |
|---|---|---|
| Home Assistant OS | — | Base OS |
| Home Assistant Core | 8123 | Smart home automation, device state |
| Prometheus | 9090 | Metrics store |
| Grafana | 3000 | Dashboards |
| Alertmanager | 9093 | Alert routing (→ Telegram) |
| node_exporter | 9100 | Host metrics for Prometheus |

## Network Position

- **IP**: 192.168.1.20/24 (static)
- **Connected to**: tp-link-switch port 4
- **DNS**: 192.168.1.21 (pi5-services AdGuard Home)
- **Local FQDN**: `monitor.home.arpa`

## Health Baseline

```yaml
health_baseline:
  interfaces: [eth0]
  services_expected_up: [homeassistant, prometheus, grafana]
  cpu_temp_c_max: 75
  disk_usage_pct_max: 85
  uptime_min_days: 7
openclaw_monitor: true
openclaw_skill: homelab/monitor-pi4-monitor
```

## Field Notes

- 2026-02-05: Migrated HA from SD card to USB SSD. Boot time dropped from 45s to 12s. No data loss.
- 2026-03-20: Added prometheus-node-exporter-lua to openwrt-primary. mwan3 metrics now visible in Grafana.
- 2026-04-10: Alertmanager Telegram integration confirmed working. Test alert fired and received within 3s.

## Related Pages

- `[[pi5-services|Raspberry Pi 5 — Services]]`
- `[[../network/ip-schema|IP Schema]]`
- `[[proxmox-main|Proxmox VE Main Server]]`

## Sources

- [Home Assistant OS](https://www.home-assistant.io/installation/raspberrypi)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)
