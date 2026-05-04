---
title: baseline Index
category: meta
tags: [index]
last_updated: 2026-04-26
---

# baseline — Master Catalog

> Agent-maintained. Run `wiki_index_rebuild` to regenerate.

## Systems

| Page | Description | Last Updated |
|---|---|---|
| [[systems/openwrt-primary\|openwrt-primary]] | OpenWrt One — primary router, gateway, mwan3 WAN failover | 2026-04-26 |
| [[systems/openwrt-standby\|openwrt-standby]] | OpenWrt on Pi 4 — standby router, LTE failover (Scheme B/C) | 2026-04-26 |
| [[systems/quectel-ec25\|quectel-ec25]] | Quectel EC25-E — LTE Cat 4 modem, shared WAN | 2026-04-26 |
| [[systems/tp-link-switch\|tp-link-switch]] | TP-Link TL-SG2008P — 8-port PoE+ managed switch | 2026-04-26 |
| [[systems/unifi-ap\|unifi-ap]] | Ubiquiti U6-Lite — WiFi 6 AP, standalone managed | 2026-04-26 |
| [[systems/proxmox-main\|proxmox-main]] | Proxmox VE 8.2 — primary compute, VMs and LXCs | 2026-04-26 |
| [[systems/pi4-monitor\|pi4-monitor]] | Raspberry Pi 4B 8GB — Home Assistant, Grafana, Prometheus | 2026-04-26 |
| [[systems/pi5-services\|pi5-services]] | Raspberry Pi 5 8GB — AdGuard Home DNS, ZeroTier, Nginx | 2026-04-26 |
| [[systems/synology-ds923\|synology-ds923]] | Synology DS923+ — NAS, SMB/NFS, Hyper Backup → B2 | 2026-04-26 |
| [[systems/tapo-hub\|tapo-hub]] | Tapo Hub H100 — IoT smart home hub (Tapo sensors) | 2026-04-26 |

## Runbooks

| Page | Description | Last Updated |
|---|---|---|
| *(none yet)* | | |

## Cheatsheets

| Page | Description | Last Updated |
|---|---|---|
| *(none yet)* | | |

## Configs

| Page | Description | Last Updated |
|---|---|---|
| *(none yet)* | | |

## Network

| Page | Description | Last Updated |
|---|---|---|
| [[network/topology\|topology]] | Full Mermaid physical/logical topology diagram | 2026-04-26 |
| [[network/routing-overview\|routing-overview]] | WAN link map and scheme transition table | 2026-04-26 |
| [[network/routing-schemes\|routing-schemes]] | Schemes A/B/C — definitions, steps, rollback | 2026-04-26 |
| [[network/ip-schema\|ip-schema]] | Static IP assignments, DHCP range, DNS | 2026-04-26 |
| [[network/dns\|dns]] | DNS architecture, local entries, AdGuard block lists | 2026-04-26 |
| [[network/zerotier\|zerotier]] | ZeroTier overlay network, members, routing rules | 2026-04-26 |

## Concepts

| Page | Description | Last Updated |
|---|---|---|
| *(none yet)* | | |

## Troubleshooting

| Page | Description | Last Updated |
|---|---|---|
| *(none yet)* | | |

## Analyses

| Page | Description | Last Updated |
|---|---|---|
| *(none yet)* | | |

## Experiments

| Page | Description | Last Updated |
|---|---|---|
| *(none yet)* | | |

## Meta

| Page | Purpose |
|---|---|
| [[meta/session-context\|Session Context]] | Active focus, open questions, pending ingests |
| [[meta/device-registry\|Device Registry]] | Machine-readable device inventory |
| [[meta/routing-state\|Routing State]] | Active WAN scheme, router status, gateway IP |
| [[meta/power-state\|Power State]] | Battery SoC, grid/solar/inverter mode, load watts |
| [[meta/vpn-state\|VPN State]] | ZeroTier/WireGuard node reachability |
| [[meta/service-state\|Service State]] | Critical services up/down/degraded |
| [[meta/backup-state\|Backup State]] | Last successful backup per target |
| [[meta/cert-state\|Certificate State]] | SSL certificate expiry dates |
| [[meta/update-state\|Update State]] | Pending firmware/package updates per device |
