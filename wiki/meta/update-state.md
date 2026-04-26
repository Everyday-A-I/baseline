---
category: meta
last_updated: YYYY-MM-DD
---

# Update State

> Agent-maintained. Updated when import scripts run or after a device is updated.
> OpenClaw uses this to stage updates safely — one device at a time, backups verified first.

```yaml
last_checked: YYYY-MM-DD HH:MM

devices:
  - slug: "<primary-router>"
    current_version: ""
    latest_available: ""
    update_available: false
    update_type: ""             # firmware | packages | security
    last_updated: ""
    notes: ""

  - slug: "<standby-router>"
    current_version: ""
    latest_available: ""
    update_available: false
    update_type: ""
    last_updated: ""
    notes: ""

  - slug: "<nas>"
    current_version: ""
    latest_available: ""
    update_available: false
    update_type: ""
    last_updated: ""
    notes: ""

  - slug: "<proxmox-node>"
    current_version: ""
    latest_available: ""
    update_available: false
    update_type: ""
    last_updated: ""
    notes: ""

policy:
  update_window: ""             # e.g. "Sundays 02:00–04:00"
  require_backup_before_update: true
  max_concurrent_updates: 1
notes: "Placeholder — add your devices and update with real values"
```

## Notes

<!-- Agent appends field notes here after update events -->
