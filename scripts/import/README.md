# Device Import Scripts

Each script collects device information and outputs a standard JSON contract to stdout.
Pipe the output to a file, then describe it to Claude:

```
"Here's the import JSON for my OpenWrt router. Create a wiki page for it."
```

Claude will create `wiki/systems/<slug>.md` with all mandatory sections pre-filled.

## Scripts

| Script | Target | Method | Requirements |
|---|---|---|---|
| `openwrt.sh` | OpenWrt router | SSH + uci export | SSH access |
| `zerotier.sh` | ZeroTier node | zerotier-cli | zerotier-one running |
| `raspberry-pi.sh` | Raspberry Pi / any SBC | SSH | SSH access |
| `proxmox.py` | Proxmox VE | REST API | API token or credentials |
| `synology.py` | Synology DSM 7+ | HTTP API | DSM credentials |
| `nodered.sh` | Node-RED | REST API | HTTP access |
| `tuya.py` | Tuya devices (local) | tinytuya scan | `pip install tinytuya` |

## Output contract

All scripts output JSON matching this shape:

```json
{
  "device_type": "openwrt",
  "slug": "openwrt-one",
  "collected_at": "2026-04-26T12:00:00Z",
  "data": { ... }
}
```

`slug` becomes the wiki page filename: `wiki/systems/<slug>.md`

## Workflow

```bash
# 1. Collect
./openwrt.sh 192.168.1.1 > /tmp/openwrt-one.json

# 2. Hand to Claude
# "Create a wiki page from scripts/import output:" then paste or reference the file

# 3. Claude creates wiki/systems/openwrt-one.md and updates:
#    - wiki/meta/device-registry.md
#    - wiki/network/topology.md
#    - wiki/index.md
#    - wiki/log.md
```

## Security notes

- Scripts **never capture or output passwords, WPA keys, or API secrets**
- UCI exports strip `password`, `secret`, `key`, `token` fields
- Synology: password is prompted interactively (not stored in shell history if omitted from CLI)
- Proxmox: use an API token scoped to read-only where possible
- Tuya: device local-control keys are noted as "key_known" but values are not exported
