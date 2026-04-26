---
category: meta
last_updated: YYYY-MM-DD
---

# Service State

> Agent-maintained. Update after any service start/stop/failure event.
> OpenClaw checks this before runbooks that depend on a specific service being up.

```yaml
last_verified: YYYY-MM-DD HH:MM

services:
  - name: home-assistant
    host: "<monitoring-sbc>"
    status: "UNKNOWN"           # up | down | degraded
    url: ""
    last_seen: ""

  - name: nodered
    host: "<monitoring-sbc>"
    status: "UNKNOWN"
    url: ""
    last_seen: ""

  - name: portainer
    host: "<proxmox-node>"
    status: "UNKNOWN"
    url: ""
    last_seen: ""

  - name: vaultwarden
    host: "<proxmox-node>"
    status: "UNKNOWN"
    url: ""
    last_seen: ""

  - name: grafana
    host: "<proxmox-node>"
    status: "UNKNOWN"
    url: ""
    last_seen: ""

notes: "Placeholder — add your services and update with real values"
```

## Notes

<!-- Agent appends field notes here when service state changes -->
