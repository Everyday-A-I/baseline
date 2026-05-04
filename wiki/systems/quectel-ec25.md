---
title: Quectel EC25 LTE Modem
category: system
tags: [lte, modem, wan, quectel, qmi]
systems: [quectel-ec25]
last_updated: 2026-04-26
version_notes: "Firmware EC25EFAR06A01M4G"
llm_threads: []
---

# Quectel EC25 LTE Modem

## Overview

Mini PCIe LTE Cat 4 modem in a USB enclosure, shared between the two routers via a powered USB hub. Provides the LTE WAN path. Connected to `openwrt-primary` (primary) as `wwan0`; a second SIM slot on the hub allows failover modem connection to `openwrt-standby` — though only one router actively sessions at a time.

## Hardware / Specs

| Field | Value |
|---|---|
| Model | Quectel EC25-E (EU/Asia bands) |
| Form factor | Mini PCIe in USB 3.0 enclosure |
| LTE category | Cat 4 (150 Mbps DL / 50 Mbps UL) |
| Bands | B1/B3/B5/B7/B8/B20/B28 |
| SIM | Nano SIM (SIM1 active) |
| Antenna | 2× external SMA (main + diversity) |
| Interface | QMI via `qmi_wwan` kernel module |

## Software Stack

| Component | Value |
|---|---|
| Kernel module | `kmod-usb-net-qmi-wwan` |
| Control tool | `uqmi` |
| mwan3 interface | `wwan0` on openwrt-primary |
| AT command port | `/dev/ttyUSB2` |

## Network Position

- No LAN IP; operates as a WAN-only device
- USB device: `1e0e:9001` (appears as `/dev/cdc-wdm0` + `/dev/ttyUSB{0-3}`)
- Connected via powered USB hub to `openwrt-primary` USB 3.0
- LTE provider: Vodafone IE (MCC 272, MNC 01)
- APN: `live.vodafone.com`

## Health Baseline

```yaml
health_baseline:
  rssi_dbm_min: -85
  rsrq_db_min: -15
  wan_ping_loss_pct_max: 3
  session_uptime_min_pct: 99
openclaw_monitor: true
openclaw_skill: homelab/monitor-quectel-ec25
```

## Field Notes

- 2026-02-10: Antenna cable on diversity port was loose; RSSI improved from -92 to -79 dBm after reseating.
- 2026-03-12: Handled 22-minute fibre outage without dropping LTE session. 0% LTE packet loss logged.
- 2026-04-01: Updated modem firmware via `AT+QFOTADL` to EC25EFAR06A01M4G.

## Related Pages

- `[[openwrt-primary|OpenWrt Primary Router]]`
- `[[openwrt-standby|OpenWrt Standby Router]]`
- `[[../network/routing-overview|Routing Overview]]`

## Sources

- [Quectel EC25 hardware guide](https://www.quectel.com/product/lte-ec25-mini-pcie)
- [OpenWrt QMI setup](https://openwrt.org/docs/guide-user/network/wan/wwan/ltedongle)
