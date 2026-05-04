---
title: ZeroTier
category: network
tags: [zerotier, vpn, overlay, remote-access]
systems: [pi5-services]
last_updated: 2026-04-26
llm_threads: []
---

# ZeroTier

## Network Details

| Field | Value |
|---|---|
| Network ID | `1d71939404b3f2b1` |
| Network name | `homelab` |
| Controller | pi5-services (192.168.1.21) — self-hosted via ZeroTier Central API |
| Managed range | 172.29.0.0/16 |
| ZeroTier version | 1.14.0 |

## Member Map

| Member Name | ZT IP | Physical Device | Purpose |
|---|---|---|---|
| `proxmox-main` | 172.29.0.10 | proxmox-main (192.168.1.10) | Remote management |
| `pi5-services` | 172.29.0.21 | pi5-services (192.168.1.21) | Controller node |
| `macbook-personal` | 172.29.0.100 | Personal MacBook | Remote admin access |
| `iphone-personal` | 172.29.0.101 | Personal iPhone | Mobile access |

## Routing Rules

ZeroTier managed routes:
- `172.29.0.0/16` → Local (ZeroTier subnet)
- `192.168.1.0/24` → 172.29.0.21 (pi5-services is the LAN gateway for remote clients)

Remote clients connecting via ZeroTier can reach the full 192.168.1.0/24 LAN by routing through pi5-services.

## Access Control

- Network is private (manual authorization required for new members)
- All traffic encrypted (Curve25519 + AES-256-GCM)
- Controller dashboard: https://my.zerotier.com (cloud auth) — note: planning migration to self-hosted Ztnet

## Related Pages

- [[pi5-services|Raspberry Pi 5 — Services]]
- [[ip-schema|IP Schema]]
- [[topology|Network Topology]]
