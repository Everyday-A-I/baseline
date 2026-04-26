---
category: meta
last_updated: YYYY-MM-DD
---

# Power State

> Agent-maintained. Update after any energy system event or configuration change.
> OpenClaw reads this before scheduling high-draw automations or firmware updates.

```yaml
last_verified: YYYY-MM-DD HH:MM
inverter_status: "UNKNOWN"      # on-grid | off-grid | passthrough | fault
battery_soc_pct: 0              # 0–100
battery_status: "UNKNOWN"       # charging | discharging | idle | float
solar_watts: 0                  # current PV input watts
load_watts: 0                   # current consumption watts
grid_status: "UNKNOWN"          # connected | disconnected | feeding-in
active_profile: "UNKNOWN"       # e.g. "ESS optimised" | "keep batteries charged" | "off-grid"
manual_override: false
notes: "Placeholder — update with real values"
```

## Notes

<!-- Agent appends field notes here when energy state changes significantly -->
