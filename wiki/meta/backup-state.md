---
category: meta
last_updated: YYYY-MM-DD
---

# Backup State

> Agent-maintained. Update after any backup job completes or fails.
> OpenClaw checks this before destructive operations — never acts if last backup is stale.

```yaml
last_verified: YYYY-MM-DD HH:MM

backups:
  - target: "<nas>"
    job: "Hyper Backup — local volumes"
    last_success: ""            # YYYY-MM-DD HH:MM
    last_status: "UNKNOWN"      # success | failed | running | never-run
    destination: ""             # e.g. "external USB" | "Synology C2" | "offsite NAS"
    retention_days: 0

  - target: "home-assistant"
    job: "HA full backup"
    last_success: ""
    last_status: "UNKNOWN"
    destination: ""
    retention_days: 0

  - target: "proxmox-vms"
    job: "Proxmox Backup Server"
    last_success: ""
    last_status: "UNKNOWN"
    destination: ""
    retention_days: 0

stale_threshold_hours: 48       # alert if any backup older than this
notes: "Placeholder — update with real values"
```

## Notes

<!-- Agent appends field notes here after backup events -->
