---
category: meta
last_updated: 2026-04-25
---

# Current Routing State

> Agent-maintained. Update after every routing scheme change.
> See [[../network/routing-schemes|Routing Schemes]] for scheme definitions.

```yaml
last_verified: 2026-04-25 00:00
active_scheme: A          # A | B | C
active_wan: "UNKNOWN — seed real data"
primary_router_status: up # up | degraded | down
standby_router_status: standby  # standby | active-wan | active-gateway
primary_dhcp_gateway: 192.168.1.1   # PLACEHOLDER — confirm actual IP
mwan3_status: active      # active | disabled | bypassed
manual_override: false
notes: "Placeholder state — update with real values before relying on this file"
```
