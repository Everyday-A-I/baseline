---
category: meta
last_updated: YYYY-MM-DD
---

# Device Registry

> Machine-readable inventory. Narrative detail lives in `wiki/systems/[slug].md`.
> Dataview can render this dynamically — see frontmatter queries.

| Hostname / Slug | Role | IP | MAC | OS / Firmware | OpenClaw Monitor | Systems Page |
|---|---|---|---|---|---|---|
| `<primary-router>` | Primary router | `<gateway-ip>` | — | OpenWrt | pending | *(not yet created)* |
| `<standby-router>` | Standby router / LTE failover | — | — | — | pending | *(not yet created)* |
| `<lte-modem>` | LTE/5G modem (WAN) | N/A | — | — | pending | *(not yet created)* |
| `<monitoring-sbc>` | SBC — monitoring, automation | — | — | — | pending | *(not yet created)* |
| `<nas>` | NAS / storage | — | — | — | pending | *(not yet created)* |

> Replace placeholders with your actual devices. Add rows freely.
> Run `wiki_index_rebuild` after adding systems pages to keep index in sync.
