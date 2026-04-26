---
category: meta
last_updated: YYYY-MM-DD
---

# VPN State

> Agent-maintained. Update after any VPN topology change or member status event.
> OpenClaw reads this before acting on a remote device — confirms it's reachable first.

```yaml
last_verified: YYYY-MM-DD HH:MM

zerotier:
  network_id: ""                # ZeroTier network ID
  controller: ""                # zerotier.com | self-hosted
  local_status: "UNKNOWN"       # online | offline | auth-pending
  members_online: []            # list of member names currently reachable
  members_offline: []           # list of member names currently unreachable
  routes_active: []             # active managed routes

wireguard:
  enabled: false
  tunnels: []                   # list of {name, peer, endpoint, status}

notes: "Placeholder — update with real values"
```

## Notes

<!-- Agent appends field notes here when VPN topology changes -->
