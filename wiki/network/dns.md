---
title: DNS
category: network
tags: [dns, adguard, local-dns, split-horizon]
systems: [pi5-services]
last_updated: 2026-04-26
llm_threads: []
---

# DNS

## Architecture

All LAN clients use `pi5-services` (192.168.1.21) as their primary DNS resolver. AdGuard Home on pi5-services handles filtering, logging, and upstream forwarding. A fallback resolver (pihole-lxc, 192.168.1.22) is configured as DHCP option 6 secondary — it forwards without filtering.

```
Client → AdGuard Home (192.168.1.21:53)
             ↓ (filtered queries blocked)
         Upstream: Cloudflare DoH (1.1.1.1) + Quad9 DoH (9.9.9.9)
```

## Local DNS Entries (AdGuard Home Custom Rules)

| Hostname | IP | Notes |
|---|---|---|
| `openwrt-primary.home.arpa` | 192.168.1.1 | Primary router |
| `openwrt-standby.home.arpa` | 192.168.1.2 | Standby router |
| `switch.home.arpa` | 192.168.1.5 | TP-Link switch |
| `proxmox.home.arpa` | 192.168.1.10 | Proxmox web UI (redirected by Nginx) |
| `monitor.home.arpa` | 192.168.1.20 | pi4-monitor |
| `dns.home.arpa` | 192.168.1.21 | pi5-services / AdGuard |
| `nas.home.arpa` | 192.168.1.30 | Synology DSM |
| `ha.home.arpa` | 192.168.1.21 | Home Assistant (via Nginx on pi5) |
| `grafana.home.arpa` | 192.168.1.21 | Grafana (via Nginx on pi5) |

## AdGuard Home — Upstream Config

```yaml
upstream_dns:
  - https://1.1.1.1/dns-query        # Cloudflare DoH
  - https://dns.quad9.net/dns-query   # Quad9 DoH
bootstrap_dns:
  - 1.1.1.1
  - 9.9.9.9
```

## Block Lists (Active)

| List | Source | Entries (approx) |
|---|---|---|
| AdGuard DNS filter | AdGuard official | ~30,000 |
| Steven Black Unified | StevenBlack/hosts | ~110,000 |

Block rate: ~24% of queries (as of 2026-04-15).

## Related Pages

- [[pi5-services|Raspberry Pi 5 — Services]]
- [[ip-schema|IP Schema]]
