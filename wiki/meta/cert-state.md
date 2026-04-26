---
category: meta
last_updated: YYYY-MM-DD
---

# Certificate State

> Agent-maintained. Update after any certificate renewal or expiry event.
> OpenClaw uses this to trigger renewal runbooks before expiry — not after.

```yaml
last_verified: YYYY-MM-DD HH:MM

certs:
  - domain: ""                  # e.g. "nas.home" | "*.yourdomain.com"
    used_by: ""                 # service or device using this cert
    issuer: ""                  # e.g. "Let's Encrypt" | "self-signed" | "internal CA"
    expiry: ""                  # YYYY-MM-DD
    days_remaining: 0           # agent recalculates on each update
    auto_renew: false
    renewal_runbook: ""         # e.g. "[[runbooks/renew-letsencrypt]]"
    last_renewed: ""

warn_days_before_expiry: 30     # surface a warning this many days before expiry
notes: "Placeholder — add your certificates and update with real values"
```

## Notes

<!-- Agent appends field notes here after renewal events -->
