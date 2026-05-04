---
title: Routing Schemes
category: network
tags: [routing, schemes, wan, failover, mwan3]
systems: [openwrt-primary, openwrt-standby, quectel-ec25]
last_updated: 2026-04-26
llm_threads: []
---

# Routing Schemes

Three named schemes cover all expected WAN states. The active scheme is always recorded in [[../meta/routing-state|routing-state.md]].

---

## Scheme A — Normal (Fully Automatic)

**Conditions**: Primary router (`openwrt-primary`) functional; mwan3 active.

- `openwrt-primary` (192.168.1.1) is the LAN gateway
- mwan3 manages Fibre ↔ LTE failover automatically:
  - WAN0 (Fibre via ETH0): weight 3 (preferred)
  - WAN1 (LTE via Quectel EC25 QMI): weight 1 (failover / load balance)
- `openwrt-standby` (192.168.1.2): connected to LAN, DHCP disabled, LTE connected but idle
- No human action required for WAN failover events

`routing-state.md` fields:
```yaml
active_scheme: A
primary_router_status: up
standby_router_status: standby
mwan3_status: active
primary_dhcp_gateway: 192.168.1.1
```

---

## Scheme B — Standby WAN via Primary Router (Partially Manual)

**Trigger**: Both primary WAN links (Fibre + LTE on `openwrt-primary`) failed or degraded. `openwrt-primary` LAN still functional. Standby LTE confirmed up.

**Steps**:
1. Confirm `openwrt-standby` LTE is up: `ssh root@192.168.1.2 'uqmi -d /dev/cdc-wdm0 --get-data-status'`
2. SSH to primary router: `ssh root@192.168.1.1`
3. Update DHCP option 3 (gateway) to standby router IP:
   ```bash
   uci set dhcp.lan.dhcp_option="3,192.168.1.2"
   uci commit dhcp
   /etc/init.d/dnsmasq restart
   # ROLLBACK: uci set dhcp.lan.dhcp_option="3,192.168.1.1" && uci commit dhcp && /etc/init.d/dnsmasq restart
   ```
4. Force renewal on critical clients:
   ```bash
   ssh michael@192.168.1.20 'sudo dhclient -r eth0 && sudo dhclient eth0'  # pi4-monitor
   ssh michael@192.168.1.21 'sudo dhclient -r eth0 && sudo dhclient eth0'  # pi5-services
   ```
5. Remaining clients recover on next DHCP lease renewal (max 12h, typically within minutes)

Runbook: [[../runbooks/scheme-b-standby-wan|scheme-b-standby-wan]]

`routing-state.md` fields:
```yaml
active_scheme: B
primary_router_status: degraded
standby_router_status: active-wan
mwan3_status: disabled
primary_dhcp_gateway: 192.168.1.2
```

---

## Scheme C — Standby Router Full Takeover (Manual, High Impact)

**Trigger**: `openwrt-primary` unresponsive (hardware failure, kernel panic, power loss with no recovery).

**Steps**:
1. Attempt to disable primary router DHCP if partially reachable:
   ```bash
   ssh root@192.168.1.1 '/etc/init.d/dnsmasq stop' || echo "Primary unreachable — skipping"
   ```
2. Enable DHCP on standby router (same subnet, same range as primary):
   ```bash
   ssh root@192.168.1.2
   uci set dhcp.lan.ignore=0
   uci set dhcp.lan.dhcp_option="3,192.168.1.2"
   uci commit dhcp
   /etc/init.d/dnsmasq restart
   # ROLLBACK: uci set dhcp.lan.ignore=1 && uci commit dhcp && /etc/init.d/dnsmasq restart
   ```
3. Standby router becomes LAN gateway at 192.168.1.2
4. Force DHCP renewal on critical clients:
   ```bash
   ssh michael@192.168.1.20 'sudo dhclient -r eth0 && sudo dhclient eth0'
   ssh michael@192.168.1.21 'sudo dhclient -r eth0 && sudo dhclient eth0'
   ssh root@192.168.1.10 'dhclient -r vmbr0 && dhclient vmbr0'
   ```
5. Wait for remaining clients to acquire leases (monitor with: `ssh root@192.168.1.2 'cat /tmp/dhcp.leases'`)

**Human approval required** — this changes the LAN gateway for all clients.

Runbook: [[../runbooks/scheme-c-primary-failure|scheme-c-primary-failure]]

`routing-state.md` fields:
```yaml
active_scheme: C
primary_router_status: down
standby_router_status: active-gateway
mwan3_status: disabled
primary_dhcp_gateway: 192.168.1.2
```

---

## Returning to Scheme A

Always follow the restore runbook — never assume the return path is obvious.

Runbook: [[../runbooks/restore-scheme-a|restore-scheme-a]]

Key steps:
1. Verify primary router is up and both WANs are functional
2. Disable DHCP on standby router (or ensure `ignore=1`)
3. Restore DHCP option 3 to 192.168.1.1 on primary router
4. Re-enable mwan3: `ssh root@192.168.1.1 '/etc/init.d/mwan3 start'`
5. Force renewal on critical clients
6. Update `routing-state.md` → `active_scheme: A`
