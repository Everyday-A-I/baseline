# baseline

**A homelab knowledge base that your AI agent maintains — structured so OpenClaw can act on it, not just read it.**

> Clone it. Point Claude Code at it. Describe your first device.
> Your wiki writes itself from there.

---

## What this is

baseline is an [Obsidian](https://obsidian.md) vault template designed to be maintained by [Claude Code](https://claude.ai/code) and consumed by [OpenClaw](https://openclaw.ai). It gives your homelab agent a persistent, structured memory — runbooks it can execute, health baselines it can monitor against, and a routing state machine it can read before touching your network.

Most homelab wikis are static. You write them, they drift, you stop trusting them.
baseline is different: the agent keeps it current as your setup evolves.

---

## Demo

> *Screenshots and screen recording coming — see the [`example`](https://github.com/Everyday-A-I/baseline/tree/example) branch for a fully populated fictional homelab.*

---

## Who this is for

You'll get the most out of this if you're running or planning to run:

- **[OpenClaw](https://openclaw.ai)** — for the agent automation layer
- **[Claude Code](https://claude.ai/code)** — for wiki maintenance (requires paid plan)
- **[Obsidian](https://obsidian.md)** — for reading and navigating the vault (free)

You don't need all three on day one. baseline is useful as a structured wiki even without the automation layer — but the OpenClaw integration is where it gets interesting.

---

## What makes this different

| | Static wiki (Wikijs, Bookstack, Notion) | baseline |
|---|---|---|
| Stays up to date | You maintain it manually | Agent updates it when things change |
| Machine-readable runbooks | No | Yes — OpenClaw can execute them |
| Routing state tracking | No | `routing-state.md` is a live state machine |
| Ingest from PDFs, chat threads, articles | Copy-paste | Structured ingest workflow with mode menu |
| Secrets integration | Varies | Password manager paths only — values never stored |

---

## What you can document

baseline has page templates for every common homelab component:

**Networking** — OpenWrt One, GL.iNet routers, 5G/LTE modems, WireGuard, ZeroTier, sing-box, VLANs, firewall rules, DNS, routing failover schemes

**Compute** — Raspberry Pi, Proxmox VE, any SBC or mini PC

**Storage** — Synology NAS, TrueNAS, any network-attached storage

**Automation & Services** — NodeRED, Home Assistant, Portainer, Vaultwarden, Grafana + Prometheus

**Smart Home & IoT** — Tuya devices (local mode, no cloud), Zigbee via Zigbee2MQTT

**Energy** — Victron EasySolar GX, solar/battery systems, smart energy plugs

**Security** — password manager secrets registry (document locations, never values)

---

## Example runbooks

baseline ships with runbook templates for procedures like these. The agent writes the full content; you approve before anything executes.

**Networking & connectivity**
- WAN failover: activate standby router LTE (Scheme B)
- Full router takeover: standby becomes LAN gateway (Scheme C)
- Return to normal routing after failover (Scheme A restore)
- ZeroTier member troubleshooting and re-authorisation
- DNS record update and propagation verification
- Firewall rule change with rollback

**Infrastructure & services**
- Proxmox VM snapshot before a risky change
- Docker container update via Portainer with rollback
- SSL/TLS certificate renewal (Let's Encrypt / ACME)
- Synology DSM update with pre-check and rollback
- Grafana dashboard backup and restore

**Data & backups**
- NAS backup job verification and integrity check
- Offsite backup sync confirmation
- Home Assistant full backup before major update

**Devices & firmware**
- Victron EasySolar GX firmware update
- OpenWrt package update with sysupgrade fallback
- New device onboarding: system page + topology + device registry in one pass

**Automation**
- NodeRED flow export and version snapshot
- Home Assistant automation audit (unused entities, stale automations)

Every runbook includes a `## Rollback` section and `requires_human_approval: true` — the agent never executes without confirmation.

---

## How it works

The vault has two layers:

```
raw/        ← your source material (PDFs, articles, transcripts) — never modified by agent
wiki/       ← the living knowledge base — agent writes here only
```

The agent (Claude Code + `CLAUDE.md`) knows how to:
- **Ingest** a vendor PDF, web article, or Claude chat thread and file it correctly
- **Create system pages** with health baselines OpenClaw can monitor against
- **Write and update runbooks** with automation metadata OpenClaw can execute
- **Track routing state** across three failover schemes (A: normal, B: standby WAN, C: full takeover)
- **Log every change** to an append-only `wiki/log.md`
- **Lint** the vault for orphan pages, broken links, and stale state

---

## Quick start

**Prerequisites:** [Obsidian](https://obsidian.md) (free), [Claude Code](https://claude.ai/code) (paid), Git

```bash
# 1. Clone as your new vault
git clone https://github.com/Everyday-A-I/baseline my-homelab-wiki
cd my-homelab-wiki

# 2. Open in Obsidian
# File → Open Vault → select the my-homelab-wiki folder
# Plugins are pre-configured — accept the prompts to enable them

# 3. Start Claude Code in the vault root
claude

# 4. Describe your first device
# "Add my Synology DS923+ NAS at 192.168.1.50 — it runs DSM 7.2,
#  has 4 bays, and is my primary backup target."

# 5. Claude creates the system page, updates the topology diagram,
#    adds it to the device registry, and logs the change.
```

Browse the [`example`](https://github.com/Everyday-A-I/baseline/tree/example) branch to see what a populated vault looks like before you start.

---

## Obsidian

baseline is built as an Obsidian vault. [Obsidian](https://obsidian.md) is a free, local-first markdown editor with a rich plugin ecosystem — your wiki is just files on disk, no vendor lock-in.

The vault comes pre-configured with four plugins:

| Plugin | Purpose |
|---|---|
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview) | Query your wiki like a database — dynamic device tables, status views |
| [Homepage](https://github.com/mirnovov/obsidian-homepage) | Opens `wiki/index.md` automatically on vault launch |
| [Excalidraw](https://github.com/zsviczian/obsidian-excalidraw-plugin) | Freehand architecture sketches embedded in pages |
| [Obsidian Git](https://github.com/denolehov/obsidian-git) | Commit and push from inside Obsidian without touching a terminal |

**Useful commands** (open the command palette with `Ctrl/Cmd + P`):

| Command | What it does |
|---|---|
| `Obsidian Git: Commit all changes` | Snapshot the vault to git |
| `Obsidian Git: Pull` | Pull latest from remote |
| `Dataview: Rebuild index` | Refresh all dynamic queries |
| `Open graph view` | Visualise connections across all wiki pages |
| `Excalidraw: Create new drawing` | Start a freehand diagram |
| `Quick switcher: Open quick switcher` | Jump to any page instantly (`Ctrl/Cmd + O`) |
| `Toggle live preview / source mode` | Switch between rendered and raw markdown |

Mermaid diagrams (topology, routing) render natively in Obsidian — no plugin required.

---

## Secrets integration

baseline documents *that* secrets exist and *where* to find them — never the values themselves. The `wiki/meta/secrets-registry.md` file is gitignored.

Works with any password manager:

- **[KeePassXC](https://keepassxc.org)** — local vault, CLI access via `keepassxc-cli`
- **[Bitwarden](https://bitwarden.com) / [Vaultwarden](https://github.com/dani-garcia/vaultwarden)** — cloud or self-hosted, CLI via `bw`
- **[1Password](https://1password.com)** — CLI via `op`

Runbooks reference secrets by path only:

```bash
# KeePassXC
keepassxc-cli show -a password ~/vault.kdbx "Homelab/<primary-router> root"

# Bitwarden / Vaultwarden
bw get password "Homelab/<primary-router> root"

# 1Password
op item get "<primary-router> root" --fields password
```

---

## OpenClaw integration

Every system page can include a `health_baseline` block:

```yaml
health_baseline:
  interfaces: [wwan0]
  wan_ping_loss_pct_max: 2
  wwan_session_min_uptime_pct: 99
openclaw_monitor: true
openclaw_skill: homelab/monitor-openwrt-one
```

Every runbook includes an `## Automation Metadata` block:

```yaml
automation:
  trigger_conditions:
    - "wwan0 interface down"
  requires_human_approval: true
  approval_timeout_seconds: 120
  estimated_impact: low
  idempotent: true
  affected_systems: [openwrt-one, quectel-rm520n]
```

OpenClaw reads `wiki/meta/routing-state.md` before any network action. It reads `wiki/meta/session-context.md` at session start. Human approval is always required before any runbook that modifies system state.

---

## Routing failover

baseline includes a three-scheme routing state machine designed for dual-WAN homelabs:

| Scheme | Condition | Action |
|---|---|---|
| **A — Normal** | All links healthy | mwan3 manages WAN failover automatically |
| **B — Standby WAN** | Primary WAN links failed | DHCP option 3 redirected to standby router's LTE |
| **C — Full takeover** | Primary router down | Standby router takes over as LAN gateway |

The agent updates `wiki/meta/routing-state.md` after every scheme change and generates the runbooks for B → A and C → A return paths.

---

## Vault structure

```
baseline/
├── CLAUDE.md                   ← agent instructions (the core of this project)
├── wiki/
│   ├── index.md                ← master catalog
│   ├── log.md                  ← append-only change log
│   ├── systems/                ← one page per device
│   ├── runbooks/               ← executable procedures
│   ├── cheatsheets/            ← quick reference
│   ├── configs/                ← annotated config snapshots
│   ├── network/                ← topology, routing, DNS, VPN, firewall
│   ├── concepts/               ← technology explanations
│   ├── troubleshooting/        ← symptom → diagnosis → resolution
│   ├── analyses/               ← architectural decisions
│   ├── experiments/            ← exploratory work
│   └── meta/                   ← device registry, routing state, session context
└── raw/                        ← source material (read-only to agent)
    ├── manuals/
    ├── articles/
    ├── assets/
    └── transcripts/
```

---

## Community

- Listed on [awesome-claws](https://github.com/machinae/awesome-claws)
- Skills registered at [openclawmap.com](https://openclawmap.com/category/skills-registry)
- Discussions: open a GitHub issue or join the [OpenClaw Discord](https://discord.com/invite/clawd)

---

## Inspiration

baseline is a homelab-specific implementation of the LLM wiki pattern described by Andrej Karpathy in [this gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the idea that an LLM should maintain a persistent, compounding wiki rather than re-synthesising knowledge from scratch on every query. The raw → wiki → schema architecture maps directly to that pattern, extended with OpenClaw integration, runbook automation, and homelab-specific page types.

---

## Licence

MIT — fork it, adapt it, make it yours.
