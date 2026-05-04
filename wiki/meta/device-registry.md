---
category: meta
last_updated: 2026-04-26
---

# Device Registry

> Machine-readable inventory. Narrative detail lives in `wiki/systems/[slug].md`.

| Hostname / Slug | Role | IP | OS / Firmware | OpenClaw Monitor | Systems Page |
|---|---|---|---|---|---|
| `openwrt-primary` | Primary router / gateway | 192.168.1.1 | OpenWrt 23.05.3 | ✓ | [[../systems/openwrt-primary\|openwrt-primary]] |
| `openwrt-standby` | Standby router / LTE failover | 192.168.1.2 | OpenWrt 23.05.3 | ✓ | [[../systems/openwrt-standby\|openwrt-standby]] |
| `quectel-ec25` | LTE modem (WAN) | N/A | EC25EFAR06A01M4G | ✓ | [[../systems/quectel-ec25\|quectel-ec25]] |
| `tp-link-switch` | Managed PoE+ switch | 192.168.1.5 | TL-SG2008P 3.0.0 | ✓ | [[../systems/tp-link-switch\|tp-link-switch]] |
| `unifi-ap` | WiFi 6 AP | 192.168.1.6 | UniFi 7.0.66 | ✓ | [[../systems/unifi-ap\|unifi-ap]] |
| `proxmox-main` | Hypervisor / compute | 192.168.1.10 | Proxmox VE 8.2 | ✓ | [[../systems/proxmox-main\|proxmox-main]] |
| `pi4-monitor` | Monitoring SBC (HA + Grafana) | 192.168.1.20 | Home Assistant OS 12.3 | ✓ | [[../systems/pi4-monitor\|pi4-monitor]] |
| `pi5-services` | Services SBC (DNS + ZT + Proxy) | 192.168.1.21 | Raspberry Pi OS Bookworm | ✓ | [[../systems/pi5-services\|pi5-services]] |
| `synology-ds923` | NAS / storage | 192.168.1.30 | DSM 7.2.1 | ✓ | [[../systems/synology-ds923\|synology-ds923]] |
| `tapo-hub` | IoT smart home hub | 192.168.1.40 | Tapo Hub 1.4.2 | ✓ | [[../systems/tapo-hub\|tapo-hub]] |
