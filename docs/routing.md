# Routing Failover

baseline includes a three-scheme routing state machine for dual-WAN homelabs. The agent tracks current state in `wiki/meta/routing-state.md` and maintains runbooks for each transition.

---

## The three schemes

| Scheme | Condition | Who acts |
|---|---|---|
| **A — Normal** | All links healthy; mwan3 managing WAN failover automatically | Automatic — no human action |
| **B — Standby WAN** | Primary WAN links failed/degraded; primary router LAN still up | Partially manual — human triggers, agent executes with approval |
| **C — Full takeover** | Primary router unresponsive / hardware failure | Manual — high impact, requires human at every step |

---

## Scheme A — Normal

- Primary router (`<primary-router>`) is LAN gateway at `<gateway-ip>`
- mwan3 manages `<lte-modem>` LTE ↔ Fibre WAN failover automatically
- Standby router connected to LAN, DHCP disabled, LTE connected but idle
- No human action required; `routing-state.md` shows `active_scheme: A`

---

## Scheme B — Standby WAN via Primary Router

**Trigger:** both primary WAN links failed/degraded; primary router LAN still functional; standby router LTE confirmed up.

**Action:** SSH to primary router → update DHCP option 3 to standby router's LAN IP → reload DHCP server. Clients fail over on next DHCP renewal or manual `dhclient` refresh.

- Primary router remains LAN gateway
- Standby router provides WAN path only
- Runbook: `[[wiki/runbooks/scheme-b-standby-wan]]`
- State: `active_scheme: B`, `standby_router_status: active-wan`

---

## Scheme C — Full Takeover

**Trigger:** primary router unresponsive / hardware failure.

**Actions (in order):**
1. Attempt to disable primary router DHCP if partially reachable
2. Enable DHCP server on standby router (same subnet, same range)
3. Standby router becomes LAN gateway
4. Force DHCP renewal on critical clients (`<monitoring-sbc>`, `<nas>`)
5. Wait for remaining clients to acquire new lease

- Runbook: `[[wiki/runbooks/scheme-c-primary-failure]]`
- State: `active_scheme: C`, `standby_router_status: active-gateway`, `primary_router_status: down`
- Impact: `high` — requires physical access flag set

---

## Returning to Scheme A

Returning from B or C to A is its own documented runbook: `[[wiki/runbooks/restore-scheme-a]]`. Never assume the return path is obvious — document it explicitly.

---

## routing-state.md

The agent updates this file after every routing action. It is the single source of truth for "what is the network doing right now" and the first thing OpenClaw reads before any network action.

```yaml
last_verified: YYYY-MM-DD HH:MM
active_scheme: A
active_wan: ""
primary_router_status: up
standby_router_status: standby
primary_dhcp_gateway: <gateway-ip>
mwan3_status: active
manual_override: false
notes: ""
```

If `last_verified` is more than 7 days old, the agent will prompt you to confirm current state during the next lint run.

---

## Extending to other topologies

The A/B/C scheme is designed for a common homelab pattern: one primary router with mwan3, one standby router with LTE. If your topology differs — multiple ISPs, BGP, VRRP — adapt the scheme names and document your own failover logic in `wiki/network/routing-schemes.md`. The state machine pattern (track current state, document transitions, require approval before changes) applies regardless of topology.
