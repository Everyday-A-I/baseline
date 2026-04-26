# Secrets Integration

baseline documents *that* secrets exist and *where* to find them — never the values themselves.

The `wiki/meta/secrets-registry.md` file is gitignored and excluded from Syncthing sync to untrusted devices. It is the only place in the vault that references secret locations — no other wiki page or runbook stores credential values.

---

## Pattern

Every runbook that needs a credential references it by password manager path only:

```bash
# KeePassXC
keepassxc-cli show -a password ~/vault.kdbx "Homelab/<primary-router> root"

# Bitwarden / Vaultwarden
bw get password "Homelab/<primary-router> root"

# 1Password
op item get "<primary-router> root" --fields password
```

The agent never prompts for or stores the master password. It assumes the vault is unlocked at session start if secret access is needed.

---

## Supported password managers

| Manager | Type | CLI | Notes |
|---|---|---|---|
| [KeePassXC](https://keepassxc.org) | Local file vault | `keepassxc-cli` | No cloud dependency; works offline |
| [Bitwarden](https://bitwarden.com) | Cloud-hosted | `bw` | Free tier available |
| [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | Self-hosted Bitwarden | `bw` | Same CLI as Bitwarden; points to your server |
| [1Password](https://1password.com) | Cloud-hosted | `op` | Strong CLI and SSH agent integration |

Any password manager with a CLI that can return a secret by path works with this pattern.

---

## secrets-registry.md format

```markdown
## Secrets Registry
<!-- Document locations only. Never values. -->

| Secret | Path | Used By |
|---|---|---|
| Primary router SSH key | Homelab/`<primary-router>` root | All router runbooks |
| Standby router SSH key | Homelab/`<standby-router>` | runbooks/scheme-b-*, scheme-c-* |
| NAS admin | Homelab/`<nas>` | systems/`<nas>`.md |
| ZeroTier API token | Homelab/ZeroTier API | network/zerotier.md |
| Proxmox root | Homelab/`<proxmox-node>` | runbooks/proxmox-* |
```

---

## Git and Syncthing exclusions

Add to your Syncthing ignore rules for the vault folder:

```
wiki/meta/secrets-registry.md
```

The `.gitignore` in baseline already excludes this file. Verify it is listed before your first `git push`.
