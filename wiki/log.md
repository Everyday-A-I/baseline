---
title: TechWiki Log
category: meta
tags: [log]
last_updated: 2026-04-26
---

# TechWiki — Append-Only Log

> Agent-maintained. Append with `wiki_log_append`. Never delete entries.
> Format: `## [YYYY-MM-DD] TYPE | Title`
> Valid TYPEs: `ingest` `query` `lint` `update` `routing` `new-system` `experiment`

---

## [2026-04-25] update | Vault initialised

Vault structure created. CLAUDE.md, index, log, and meta seed files written.
Pending: real device and network content to be seeded by user.

---

## [2026-04-26] new-system | Example homelab — 10 devices seeded

Added example content branch with a fictional 10-device homelab:

**Systems created:**
- openwrt-primary (OpenWrt One, primary router)
- openwrt-standby (OpenWrt on Pi 4, standby/failover)
- quectel-ec25 (LTE modem)
- tp-link-switch (TL-SG2008P managed switch)
- unifi-ap (UniFi U6-Lite WiFi 6 AP)
- proxmox-main (Proxmox VE, i5-12400, 64GB)
- pi4-monitor (Pi 4B 8GB — Home Assistant, Grafana, Prometheus)
- pi5-services (Pi 5 8GB — AdGuard Home DNS, ZeroTier, Nginx)
- synology-ds923 (DS923+ NAS)
- tapo-hub (Tapo H100 IoT hub)

**Network pages created:** topology, routing-overview, routing-schemes, ip-schema, dns, zerotier

**State:** routing-state.md set to Scheme A (normal, fibre primary + LTE standby).

All devices have `openclaw_monitor: true` and populated `health_baseline` blocks.
