# baseline

**A homelab knowledge base that your AI agent maintains — structured so OpenClaw can act on it, not just read it.**

> Point Claude Code at this repo. It handles most of the setup.
> Then build your wiki conversationally — your agent earns autonomy as you gain trust in it.

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

## Getting started

### How setup works

Point Claude Code at this repo and say `"Set up baseline"`. It will:

- Run `setup.sh` — creates a Python venv, installs MCP dependencies, writes `.mcp.json` with correct absolute paths for your machine
- Tell you exactly what it did and what you need to do next

**You then restart Claude Code** (MCP servers load at startup — this step cannot be automated) and return to continue.

| Step | Who |
|---|---|
| Clone repo, run `claude`, say "Set up baseline" | **You** |
| Run `setup.sh`, verify paths, write `.mcp.json` | Claude Code |
| Restart Claude Code | **You** — required, cannot be skipped |
| Verify MCP tools loaded, run smoke test | Claude Code |
| Open vault in Obsidian, enable plugins | **You** — GUI, cannot be automated |
| Describe your first device | **You** |
| Create system page, update topology, log change | Claude Code |

---

### Phase 1 — Installation

```bash
git clone https://github.com/Everyday-A-I/baseline my-homelab-wiki
cd my-homelab-wiki
claude
```

Then tell Claude Code:

> **"Set up baseline"**

Claude runs `setup.sh`, which installs dependencies, writes `.mcp.json`, and prints a summary. Review the output — confirm the paths look correct for your system.

> ⚠️ **Human action required:** Restart Claude Code.
> MCP servers are loaded at startup. The wiki tools are not available until you restart.

After restarting, return to the vault and say:

> **"Verify my baseline setup"**

Claude will call `wiki_list` as a smoke test and confirm the MCP tools are live. If anything is wrong it will tell you what to fix.

---

### Phase 2 — Build your wiki

With the MCP confirmed, describe your homelab conversationally. Start simple:

> **"Add my primary router — it's an OpenWrt One at 192.168.1.1, running OpenWrt 24.x, and it's the LAN gateway with mwan3 managing WAN failover."**

Claude creates `wiki/systems/openwrt-one.md`, updates `wiki/network/topology.md`, adds the device to `wiki/meta/device-registry.md`, and logs the change.

**Review every page Claude creates** before adding more devices. This is how you build trust in the agent's output — and catch anything that doesn't match your setup.

Work through your devices one at a time. For each one, Claude will:
- Create the system page with all mandatory sections
- Ask clarifying questions if specs are missing
- Update the topology diagram
- Log the change

> ⚠️ **Human action required:** Read and approve each page before proceeding.
> Don't rush this phase. A well-seeded wiki is the foundation everything else depends on.

---

### Phase 3 — Ingest documentation

Once your devices are documented, start ingesting source material. Drop vendor PDFs, web articles, or paste Claude chat thread URLs.

> **"Ingest raw/manuals/openwrt-one-quickstart.pdf"**
> **"Ingest this thread: https://claude.ai/share/..."**

Claude always presents an **Ingest Mode Menu** before writing anything:

```
A) Full synthesis    — extract all decisions and configs into structured pages
B) Decision log only — extract architectural choices as an analysis entry
C) Runbook extraction — identify procedures; draft as runbook stubs for review
D) Raw summary only  — summarise to raw/articles/; flag pages to update later
E) Review first      — show proposed structure; write nothing until you confirm
```

> ⚠️ **Human action required:** Choose the ingest mode. Option E (Review first) is recommended until you're confident in how the agent structures content.

---

### Phase 4 — Write and review runbooks

Runbooks are the bridge between the wiki and OpenClaw automation. The agent drafts them; you decide when they're ready to be executed.

> **"Draft a runbook for activating the standby router's LTE when primary WAN fails."**

Claude drafts the runbook with all mandatory sections: Purpose, Prerequisites, Automation Metadata, Steps, Verification, Rollback, Known Pitfalls.

> ⚠️ **Human action required:** Read every runbook — especially `## Steps` and `## Rollback` — before it's considered live.
> Pay particular attention to:
> - The exact commands in `## Steps`
> - That every action has a `# ROLLBACK:` comment immediately below it
> - The `estimated_impact` level in Automation Metadata
> - That `requires_human_approval: true` is set (it always should be)

Do not connect OpenClaw to runbooks you haven't read in full.

---

### Phase 5 — OpenClaw integration

Once you have system pages with `health_baseline` blocks and at least a few reviewed runbooks, connect OpenClaw.

Install and configure [OpenClaw](https://openclaw.ai), then point its skills at your wiki:

- `wiki/meta/routing-state.md` — OpenClaw reads this before any network action
- `wiki/meta/session-context.md` — loaded at session start
- `wiki/systems/*.md` pages with `openclaw_monitor: true` — polled by corresponding skills

> ⚠️ **Human action required:** Test each OpenClaw skill manually before enabling monitoring.
> Run the skill, observe what it reads and proposes, confirm it interprets your wiki correctly.

---

### Phase 6 — Supervised automation

With OpenClaw connected and skills verified, the system reaches its intended state: your agent monitors your homelab, detects issues against documented baselines, and proposes runbook executions — which you approve before anything runs.

**This approval gate is permanent.** Every runbook has `requires_human_approval: true`. OpenClaw will always present the proposed commands, affected systems, and impact level via your configured channel (Telegram, Discord, etc.) before executing.

The progression looks like this:

```
Week 1-2:  Wiki populated, all pages reviewed by you
Week 3-4:  Runbooks drafted and read; test ingests working
Month 2:   OpenClaw connected; skills tested manually
Month 2+:  Supervised automation — you approve each execution
Ongoing:   Trust builds; approval becomes a quick confirmation, not a review
```

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

## MCP setup (reference)

baseline requires one MCP server: **`wiki_mcp.py`**, included in this repo. `setup.sh` handles installation automatically. This section is reference only — you don't need to read it to get started.

**What wiki_mcp provides:**

| Tool | Purpose |
|---|---|
| `wiki_search` | BM25 full-text search across all wiki pages |
| `wiki_read` | Read any file within the vault |
| `wiki_write` | Create or overwrite a page (auto-backup before write) |
| `wiki_patch` | Append or replace a named section without rewriting the page |
| `wiki_list` | List pages, optionally filtered by category |
| `wiki_index_rebuild` | Regenerate `wiki/index.md` from current vault state |
| `wiki_log_append` | Append a timestamped entry to `wiki/log.md` |
| `wiki_lint` | Health-check: orphans, broken links, missing frontmatter |
| `wiki_ingest_raw` | Read raw source files — markdown or PDF with page numbers |

**Key libraries:**

| Library | Purpose |
|---|---|
| [`fastmcp`](https://github.com/jlowin/fastmcp) | MCP server framework |
| [`rank-bm25`](https://github.com/dorianbrown/rank_bm25) | Full-text search over wiki pages |
| [`python-frontmatter`](https://github.com/eyeseast/python-frontmatter) | YAML frontmatter read/write |
| [`pymupdf`](https://pymupdf.readthedocs.io) | PDF text extraction with page numbers (optional) |

**Manual install** (if not using `setup.sh`):

```bash
python3 -m venv ~/.venvs/baseline
~/.venvs/baseline/bin/pip install mcp[cli] fastmcp rank_bm25 python-frontmatter pymupdf
```

Then edit `.mcp.json` in the vault root — replace the template paths with your actual venv and vault locations. Use the full path to the venv's `python` binary (bare `python` is unreliable across systems).

**Without Claude Code — Claude Desktop or Claude web:**

The full workflow runs on **Claude Desktop** without Claude Code:
- `wiki_mcp.py` tools work identically
- Paste `CLAUDE.md` content into your Project's system prompt
- Git commits are handled by the [Obsidian Git](https://github.com/denolehov/obsidian-git) plugin
- If the agent needs to access files outside the vault, add the [Filesystem MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)

**Claude web** works for queries and ingests but git is fully manual and session constraints make long maintenance runs awkward. Claude Desktop is the better non-CC option.

---

## Obsidian

baseline is built as an Obsidian vault. [Obsidian](https://obsidian.md) is a free, local-first markdown editor — your wiki is plain markdown files on disk, no vendor lock-in.

The vault comes pre-configured with four plugins:

| Plugin | Purpose |
|---|---|
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview) | Query your wiki like a database — dynamic device tables, status views |
| [Homepage](https://github.com/mirnovov/obsidian-homepage) | Opens `wiki/index.md` automatically on vault launch |
| [Excalidraw](https://github.com/zsviczian/obsidian-excalidraw-plugin) | Freehand architecture sketches embedded in pages |
| [Obsidian Git](https://github.com/denolehov/obsidian-git) | Commit and push from inside Obsidian without a terminal |

Obsidian is the reading interface — you don't need it for the agent workflow, but it makes navigating a populated wiki significantly easier.

**Useful commands** (`Ctrl/Cmd + P`):

| Command | What it does |
|---|---|
| `Obsidian Git: Commit all changes` | Snapshot the vault to git |
| `Obsidian Git: Pull` | Pull latest from remote |
| `Dataview: Rebuild index` | Refresh all dynamic queries |
| `Open graph view` | Visualise connections across all wiki pages |
| `Quick switcher: Open quick switcher` | Jump to any page (`Ctrl/Cmd + O`) |
| `Toggle live preview / source mode` | Switch between rendered and raw markdown |

Mermaid diagrams (topology, routing) render natively — no plugin required.

---

## Secrets integration

baseline documents *that* secrets exist and *where* to find them — never the values themselves. The `wiki/meta/secrets-registry.md` file is gitignored.

Works with any password manager:

- **[KeePassXC](https://keepassxc.org)** — local vault, CLI via `keepassxc-cli`
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

OpenClaw reads `wiki/meta/routing-state.md` before any network action. It reads `wiki/meta/session-context.md` at session start. Human approval is always required before any runbook that modifies system state — this is a permanent constraint, not a training-wheels setting.

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
├── wiki_mcp.py                 ← MCP server (run via .mcp.json; do not edit unless extending)
├── .mcp.json                   ← MCP config template (setup.sh writes your real paths here)
├── setup.sh                    ← run once after cloning; handles venv, deps, .mcp.json
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
