---
title: IP Schema
category: network
tags: [ip, dhcp, static, vlan, dns]
systems: []
last_updated: 2026-04-26
llm_threads: []
---

# IP Schema

## LAN Summary

| Field | Value |
|---|---|
| Subnet | 192.168.1.0/24 |
| Gateway (Scheme A) | 192.168.1.1 (openwrt-primary) |
| Gateway (Scheme B/C) | 192.168.1.2 (openwrt-standby) |
| DNS primary | 192.168.1.21 (pi5-services, AdGuard Home) |
| DNS fallback | 192.168.1.22 (proxmox-main LXC: pihole-lxc) |
| DHCP range (dynamic) | 192.168.1.50 – 192.168.1.199 |
| DHCP server | openwrt-primary (dnsmasq) |

## Static Assignments

| IP | Hostname / Slug | Device | Assigned Via |
|---|---|---|---|
| 192.168.1.1 | openwrt-primary | OpenWrt One | Interface config |
| 192.168.1.2 | openwrt-standby | Raspberry Pi 4 (OpenWrt) | Interface config |
| 192.168.1.5 | tp-link-switch | TL-SG2008P | DHCP static lease (MAC) |
| 192.168.1.6 | unifi-ap | U6-Lite | DHCP static lease (MAC) |
| 192.168.1.10 | proxmox-main | i5-12400 server | Interface config |
| 192.168.1.20 | pi4-monitor | Raspberry Pi 4B 8GB | Interface config |
| 192.168.1.21 | pi5-services | Raspberry Pi 5 8GB | Interface config |
| 192.168.1.22 | pihole-lxc | Proxmox LXC 100 | Interface config |
| 192.168.1.23 | monitoring-lxc | Proxmox LXC 101 | Interface config |
| 192.168.1.24 | dev-ubuntu | Proxmox VM 201 | Interface config |
| 192.168.1.30 | synology-ds923 | DS923+ | Interface config |
| 192.168.1.40 | tapo-hub | Tapo H100 | DHCP static lease (MAC) |

## DHCP Dynamic Range (192.168.1.50–199)

Devices without static assignments (laptops, phones, guests, IoT sensors via WiFi).

Lease time: 12 hours.

## ZeroTier Overlay Network

See [[zerotier|ZeroTier]] for ZeroTier IP assignments (172.29.x.x range).

## Future: IoT VLAN

Planned: separate IoT VLAN (VLAN 10, 192.168.10.0/24) to isolate Tapo devices and guest WiFi. Blocked on: UniFi standalone VLAN support testing.
