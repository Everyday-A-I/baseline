---
title: Network Topology
category: network
tags: [topology, mermaid, lan, wan]
systems: [openwrt-primary, openwrt-standby, tp-link-switch, unifi-ap, proxmox-main, pi4-monitor, pi5-services, synology-ds923, tapo-hub, quectel-ec25]
last_updated: 2026-04-26
llm_threads: []
---

# Network Topology

> Agent-maintained. Regenerate the full Mermaid block after any topology change.
> See [[../meta/routing-state|routing-state]] for current active scheme.

## Physical / Logical Diagram

```mermaid
graph TD
    subgraph WAN
        FIBRE[Fibre ISP ONT]
        LTE[LTE Network]
    end

    subgraph Routers
        RP[openwrt-primary\n192.168.1.1\nGateway]
        RS[openwrt-standby\n192.168.1.2\nStandby]
        MOD[quectel-ec25\nUSB LTE modem]
    end

    subgraph Core["Core Switch — tp-link-switch (192.168.1.5)"]
        SW[8-port PoE+ Managed]
    end

    subgraph Servers
        PVE[proxmox-main\n192.168.1.10\nProxmox VE]
        NAS[synology-ds923\n192.168.1.30\nNAS]
    end

    subgraph SBCs
        MON[pi4-monitor\n192.168.1.20\nHA + Grafana]
        SVC[pi5-services\n192.168.1.21\nDNS + ZT + Proxy]
    end

    subgraph Wireless
        AP[unifi-ap\n192.168.1.6\nWiFi 6]
        IOT[tapo-hub\n192.168.1.40\nIoT Hub]
    end

    FIBRE -->|ETH0 WAN| RP
    MOD -->|USB QMI| RP
    MOD -.->|USB QMI idle| RS
    LTE --> MOD

    RP -->|port 1| SW
    RS -->|port 2| SW
    PVE -->|port 3| SW
    MON -->|port 4 PoE| SW
    NAS -->|ports 5+6 LACP| SW
    SVC -->|port 7| SW
    AP -->|port 8 PoE| SW

    AP -.->|WiFi homelab-iot| IOT
```

## State Machine Links

- Active routing scheme: [[../meta/routing-state|routing-state.md]]
- IP assignments: [[ip-schema|IP Schema]]
- WAN failover logic: [[routing-overview|Routing Overview]]
- ZeroTier overlay: [[zerotier|ZeroTier]]
