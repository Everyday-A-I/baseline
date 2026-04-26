# OpenClaw Integration

baseline is the knowledge layer for an [OpenClaw](https://openclaw.ai) homelab agent. OpenClaw reads the wiki to understand the network, monitors devices against documented baselines, and proposes runbook executions — which you approve before anything runs.

---

## How it connects

Three files are the primary interface between baseline and OpenClaw:

| File | OpenClaw reads it to... |
|---|---|
| `wiki/meta/routing-state.md` | Understand current network state before any network action |
| `wiki/meta/session-context.md` | Orient itself at session start |
| `wiki/systems/*.md` (with `openclaw_monitor: true`) | Know what to monitor and what "healthy" looks like |

OpenClaw skill files live at `~/.openclaw/skills/homelab/` on the host machine — not in this vault. The `openclaw_skill` frontmatter field on each wiki page records the corresponding skill name for cross-reference.

---

## System page health baselines

Every system page that OpenClaw monitors needs a `health_baseline` block:

```yaml
health_baseline:
  interfaces: [wwan0]
  wan_ping_loss_pct_max: 2
  rssi_dbm_min: -85
  wwan_session_min_uptime_pct: 99
openclaw_monitor: true
openclaw_skill: homelab/monitor-openwrt-one
```

OpenClaw compares live metrics against these values. A mismatch surfaces a proposed runbook — it does not act autonomously.

---

## Runbook automation metadata

Every runbook that OpenClaw may invoke needs an `## Automation Metadata` section:

```yaml
automation:
  trigger_conditions:
    - "wwan0 interface down"
  requires_human_approval: true   # always true — no exceptions
  approval_timeout_seconds: 120   # agent aborts if no response
  estimated_impact: low           # low | medium | high
  idempotent: true                # safe to run twice without harm
  rollback: "See ## Rollback"
  openclaw_skill: homelab/reconnect-wwan
  affected_systems: [openwrt-one, quectel-rm520n]
  requires_physical_access: false
```

Rules:
- `requires_human_approval` is **always `true`**. This is not a setting to change when you "trust the agent enough" — it is a permanent architectural constraint.
- `estimated_impact: high` runbooks must explicitly set `requires_physical_access`.
- Every `## Steps` action must have a `# ROLLBACK:` comment immediately below it.

---

## Human approval gate

When OpenClaw proposes a runbook execution, it sends an approval message to your configured channel (Telegram, Discord, WhatsApp) containing:

- Runbook name
- Exact commands to be run
- Affected systems
- Estimated impact level
- Approval timeout

You approve or deny. If no response within `approval_timeout_seconds`, the agent aborts.

**This gate is permanent.** It does not become optional as the system matures.

---

## Live state files

OpenClaw reads these meta files to understand current state before acting:

| File | Tracks |
|---|---|
| `meta/routing-state.md` | Active WAN scheme, router status, gateway IP |
| `meta/power-state.md` | Battery SoC, grid/solar/inverter mode, load |
| `meta/vpn-state.md` | ZeroTier/WireGuard node reachability |
| `meta/service-state.md` | Critical service up/down status |
| `meta/backup-state.md` | Last successful backup per target |
| `meta/cert-state.md` | SSL certificate expiry dates |
| `meta/update-state.md` | Pending firmware/package updates |

The agent updates the relevant file after any action that changes state. See [State Files](../wiki/meta/) for current values.

---

## Connecting OpenClaw

After your wiki is populated and runbooks reviewed (see [Getting Started](../README.md#phase-5--openclaw-integration)):

1. Install OpenClaw — see [openclaw.ai](https://openclaw.ai)
2. Configure your messaging channel (Telegram recommended for homelab use)
3. Create a skill file at `~/.openclaw/skills/homelab/` for each `openclaw_skill` referenced in your wiki
4. Point the skill at `wiki/meta/routing-state.md` and the relevant system pages
5. Test each skill manually before enabling scheduled monitoring

Join the [OpenClaw Discord](https://discord.com/invite/clawd) for skill examples and community support.
