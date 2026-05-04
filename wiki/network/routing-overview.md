---
title: Routing Overview
category: network
tags: [routing, wan, mwan3, failover, mermaid]
systems: [openwrt-primary, openwrt-standby, quectel-ec25]
last_updated: 2026-04-26
llm_threads: []
---

# Routing Overview

> Agent-maintained. Regenerate full Mermaid block after any routing change.
> See [[../meta/routing-state|routing-state.md]] for live state.
> Full scheme definitions: [[routing-schemes|Routing Schemes]].

## WAN Link Map (Scheme A — Normal)

```mermaid
graph LR
    subgraph WAN Links
        FIBRE[Fibre\nISP ONT\n~500 Mbps]
        LTE[LTE\nVodafone IE\n~80 Mbps]
    end

    subgraph Primary Router ["openwrt-primary (192.168.1.1)"]
        MWAN[mwan3\npolicy: balanced\nfailover ready]
        DHCP_P[DHCP server\noption 3 = 192.168.1.1]
    end

    subgraph Standby Router ["openwrt-standby (192.168.1.2)"]
        LTE_S[LTE connected\nidle — not routing]
        DHCP_S[DHCP server\nDISABLED]
    end

    LAN[LAN clients\n192.168.1.0/24]

    FIBRE -->|WAN0 primary| MWAN
    LTE -->|WAN1 secondary| MWAN
    MWAN --> DHCP_P
    DHCP_P -->|gateway| LAN
    LTE_S -.->|standby path| Standby Router
```

## Scheme Transitions

| From | To | Trigger | Runbook |
|---|---|---|---|
| A | A | mwan3 auto-failover (WAN link failure) | Automatic — no runbook needed |
| A | B | Both primary WANs failed; standby LTE up | [[../runbooks/scheme-b-standby-wan\|Scheme B]] |
| A | C | Primary router unresponsive | [[../runbooks/scheme-c-primary-failure\|Scheme C]] |
| B or C | A | Primary router and WANs restored | [[../runbooks/restore-scheme-a\|Restore Scheme A]] |

## Current State

See [[../meta/routing-state|routing-state.md]] — agent updates this file after every routing change.
