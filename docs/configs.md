# wiki/configs — Annotated Config Reference

`wiki/configs/` stores annotated snapshots of configuration files — documented records of how things are set up **when everything is working**, with notes explaining the non-obvious decisions.

---

## What it is

Each config page is a point-in-time snapshot of a config file or settings block, annotated inline to explain:
- Why non-default values were chosen
- What breaks if a value changes
- Which other systems depend on this setting

Example: `configs/openwrt-mwan3.md` documents the mwan3 interface tracking config with annotations explaining why the ping targets and intervals are set as they are.

---

## What it is not

| Not this | Use instead |
|---|---|
| A backup system | Git history provides that |
| Pre-change snapshots | Runbook `## Rollback` sections capture the before-state |
| A place to store raw `.conf` files | Those go in `raw/` |
| An automated backup target | That's `wiki/runbooks/nas-backup-verify.md` |

---

## Page format

```markdown
---
title: <System> — <Component> Config
category: config
tags: [system-slug, component]
systems: [system-slug]
last_updated: YYYY-MM-DD
version_notes: "firmware/software version this applies to"
---

## Context
What this config is for; what version it applies to; when it was last verified.

## Full Config
\`\`\`
# annotated config block
setting = value   # why this value; what breaks if changed
\`\`\`

## Key Parameters
| Parameter | Value | Rationale |
|---|---|---|
| ... | ... | ... |

## Related Runbooks
- [[runbooks/relevant-runbook]]

## Sources
- [[raw/manuals/vendor-doc.pdf#page=12|Vendor doc §3]]
```

---

## Good candidates

- Router: mwan3 failover config, DHCP options, firewall rules rationale
- Victron: ESS assistant settings, grid feed-in limits, battery charge profile
- Proxmox: VM/LXC resource allocations, storage pool config
- Synology: Hyper Backup task settings, shared folder permissions
- NodeRED: settings.js (logging, admin auth, custom nodes path)
- WireGuard/ZeroTier: peer config, routing rules

---

## Keeping configs current

The agent updates a config page when:
- A runbook changes the config and succeeds
- A Field Note on the system page records a manual config change
- An ingest of a vendor changelog flags a setting that should be reviewed

Config pages are not automatically synced from devices — they reflect the last time a human or runbook verified the config. The `version_notes` frontmatter field records what firmware/software version the config was verified against.
