# baseline

**A homelab knowledge base that your AI agent maintains — structured so OpenClaw can act on it, not just read it.**

> Point Claude Code at this repo. It handles most of the setup.
> Then build your wiki conversationally — your agent earns autonomy as you gain trust in it.

---

## What this is

baseline is an [Obsidian](https://obsidian.md) vault template designed to be maintained by [Claude Code](https://claude.ai/code) and consumed by [OpenClaw](https://openclaw.ai). It gives your homelab agent a persistent, structured memory — runbooks it can execute, health baselines it can monitor against, and live state files it reads before touching anything.

**The wiki lives on your machine** as plain markdown files. Obsidian reads it locally. The Obsidian Git plugin commits changes and pushes to your GitHub remote as a versioned backup. Syncthing (optional) keeps it in sync across devices in real time. Nothing requires a cloud account to function.

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
| Machine-readable runbooks | No | Yes — OpenClaw can execute them with your approval |
| Live state tracking | No | Routing, power, VPN, services, backups, certs, updates |
| Ingest from PDFs, chat threads, articles | Copy-paste | Structured ingest workflow with mode menu |
| Secrets integration | Varies | Password manager paths only — values never stored |

---

## What you can document

**Networking** — OpenWrt One, GL.iNet routers, 5G/LTE modems, WireGuard, ZeroTier, sing-box, VLANs, firewall rules, DNS, routing failover schemes

**Compute** — Raspberry Pi, Proxmox VE, any SBC or mini PC

**Storage** — Synology NAS, TrueNAS, any network-attached storage

**Automation & Services** — NodeRED, Home Assistant, Portainer, Vaultwarden, Grafana + Prometheus

**Smart Home & IoT** — Tuya devices (local mode, no cloud), Zigbee via Zigbee2MQTT

**Energy** — Victron EasySolar GX, solar/battery systems, smart energy plugs

**Security** — password manager secrets registry (document locations, never values)

---

## Getting started

### How setup works

Point Claude Code at this repo and say `"Set up baseline"`. It will run `setup.sh`, which:
- Checks Python 3.10+
- Creates a dedicated venv at `~/.venvs/baseline`
- Installs MCP dependencies
- Writes `.mcp.json` with correct absolute paths for your machine

You then restart Claude Code (MCP servers load at startup — this cannot be automated) and return to continue.

| Step | Who |
|---|---|
| Clone repo, run `claude`, say "Set up baseline" | **You** |
| Run `setup.sh`, verify paths, write `.mcp.json` | Claude Code |
| Restart Claude Code | **You** — required, cannot be skipped |
| Verify MCP tools loaded, run smoke test | Claude Code |
| Open vault in Obsidian, enable plugins | **You** — GUI, cannot be automated |
| Describe your first device | **You** |
| Create system page, update topology, log change | Claude Code |

```bash
git clone https://github.com/Everyday-A-I/baseline my-homelab-wiki
cd my-homelab-wiki
claude
# say: "Set up baseline"
```

→ See [docs/mcp-setup.md](docs/mcp-setup.md) for manual installation and multi-vault configuration.

---

### Phase 1 — Installation

After cloning and running `claude`, say:

> **"Set up baseline"**

Claude runs `setup.sh` and prints a summary. Review the output — confirm the paths look correct. Then:

> ⚠️ **Human action required: restart Claude Code.**
> MCP servers load at startup. Wiki tools are not available until you restart.

After restarting, say:

> **"Verify my baseline setup"**

Claude calls `wiki_list` as a smoke test and confirms the tools are live.

---

### Phase 2 — Build your wiki

Describe your homelab conversationally, one device at a time:

> **"Add my primary router — OpenWrt One at 192.168.1.1, running OpenWrt 24.x, LAN gateway with mwan3 failover."**

Claude creates the system page, updates the topology diagram, adds the device to the registry, and logs the change.

> ⚠️ **Human action required: read every page Claude creates before adding the next device.**
> A well-seeded wiki is the foundation everything else depends on. Don't rush this phase.

---

### Phase 3 — Ingest documentation

Drop PDFs, articles, or Claude chat thread URLs into the vault:

> **"Ingest raw/manuals/openwrt-one-quickstart.pdf"**

Claude always presents an **Ingest Mode Menu** before writing anything:

```
A) Full synthesis    — extract all decisions and configs into structured pages
B) Decision log only — architectural choices as an analysis entry only
C) Runbook extraction — identify procedures; draft stubs for your review
D) Raw summary only  — summarise to raw/articles/; flag pages to update later
E) Review first      — show proposed structure; write nothing until confirmed
```

> ⚠️ **Human action required: choose the ingest mode.** Option E recommended until you're confident in how the agent structures content.

---

### Phase 4 — Write and review runbooks

> **"Draft a runbook for activating standby LTE when primary WAN fails."**

Claude drafts the runbook with all mandatory sections.

> ⚠️ **Human action required: read every runbook in full before it's considered live.**
> Check `## Steps`, every `# ROLLBACK:` comment, and `estimated_impact`.
> Do not connect OpenClaw to runbooks you haven't read.

---

### Phase 5 — OpenClaw integration

Once you have reviewed system pages and runbooks, connect OpenClaw. Test each skill manually before enabling monitoring.

> ⚠️ **Human action required: verify each OpenClaw skill reads your wiki correctly before enabling it.**

→ See [docs/openclaw.md](docs/openclaw.md) for connection details and skill setup.

---

### Phase 6 — Supervised automation

OpenClaw monitors your homelab, detects issues against documented baselines, and proposes runbook executions — which you approve before anything runs.

**The approval gate is permanent.** `requires_human_approval: true` is an architectural constraint, not a training-wheels setting.

```
Week 1–2:  Wiki populated; all pages reviewed by you
Week 3–4:  Runbooks drafted and read; test ingests working
Month 2:   OpenClaw connected; skills tested manually
Month 2+:  Supervised automation — you approve each execution
Ongoing:   Trust builds; approval becomes a quick confirm, not a review
```

---

## Example runbooks

The agent drafts these from your descriptions; you approve before anything executes.

**Networking & connectivity** — WAN failover (Scheme B), full router takeover (Scheme C), restore normal routing (Scheme A), ZeroTier re-authorisation, DNS update, firewall rule change with rollback

**Infrastructure & services** — Proxmox VM snapshot, Docker container update with rollback, SSL/TLS renewal, Synology DSM update, Grafana dashboard backup

**Data & backups** — NAS backup verification, offsite sync confirmation, Home Assistant backup

**Devices & firmware** — Victron EasySolar GX firmware update, OpenWrt sysupgrade, new device onboarding (system page + topology + registry in one pass)

**Automation** — NodeRED flow export, Home Assistant automation audit

Every runbook includes `## Rollback` and `requires_human_approval: true`.

→ See [docs/routing.md](docs/routing.md) for the full routing failover state machine.

---

## Live state files

baseline tracks seven categories of state in `wiki/meta/`. These are agent-maintained files that OpenClaw reads before acting — a snapshot of "what is the homelab doing right now."

| File | Tracks |
|---|---|
| `meta/routing-state.md` | Active WAN scheme, router status, gateway IP |
| `meta/power-state.md` | Battery SoC, grid/solar/inverter mode, load watts |
| `meta/vpn-state.md` | ZeroTier/WireGuard node reachability |
| `meta/service-state.md` | Critical services up/down/degraded |
| `meta/backup-state.md` | Last successful backup per target |
| `meta/cert-state.md` | SSL certificate expiry dates |
| `meta/update-state.md` | Pending firmware/package updates per device |

The agent updates the relevant file after any action that changes state.

---

## Vault structure

```
baseline/
├── CLAUDE.md                   ← agent instructions (the core of this project)
├── wiki_mcp.py                 ← MCP server (run via .mcp.json)
├── .mcp.json                   ← MCP config template (setup.sh writes real paths here)
├── setup.sh                    ← run once after cloning
├── docs/                       ← reference documentation
│   ├── mcp-setup.md
│   ├── obsidian.md
│   ├── openclaw.md
│   ├── routing.md
│   ├── secrets.md
│   └── configs.md
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── systems/
│   ├── runbooks/
│   ├── cheatsheets/
│   ├── configs/                ← annotated config snapshots (see docs/configs.md)
│   ├── network/
│   ├── concepts/
│   ├── troubleshooting/
│   ├── analyses/
│   ├── experiments/
│   └── meta/                   ← live state files + device registry + session context
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
