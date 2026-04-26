#!/usr/bin/env bash
# Import ZeroTier network state from a host running zerotier-one.
# Outputs JSON to stdout; hand to Claude for wiki/network/zerotier.md creation.
#
# Usage: ./zerotier.sh [host]
#   host defaults to localhost; pass an SSH target to collect from a remote host
#
# Requirements (local mode): zerotier-cli in PATH, sudo if needed
# Requirements (remote mode): SSH access, zerotier-cli installed on remote

set -euo pipefail

HOST="${1:-}"
collected_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ -n "$HOST" ]; then
  ZT="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 ${HOST} sudo zerotier-cli"
else
  # Try without sudo first, fall back
  if zerotier-cli info &>/dev/null; then
    ZT="zerotier-cli"
  else
    ZT="sudo zerotier-cli"
  fi
fi

info=$($ZT info 2>/dev/null || echo "error: zerotier-cli not reachable")
node_id=$(echo "$info" | awk '{print $3}')
version=$(echo "$info" | awk '{print $4}')
status=$(echo "$info" | awk '{print $5}')

networks_json=$($ZT listnetworks -j 2>/dev/null || echo "[]")
peers_json=$($ZT listpeers -j 2>/dev/null || echo "[]")

python3 - <<PYEOF
import json, sys

try:
    networks = json.loads("""${networks_json}""")
except Exception:
    networks = []

try:
    peers = json.loads("""${peers_json}""")
except Exception:
    peers = []

# Summarise peers by role
controllers = [p for p in peers if p.get("role") == "CONTROLLER"]
leaves = [p for p in peers if p.get("role") == "LEAF"]
online_leaves = [p for p in leaves if p.get("latency", -1) >= 0]

data = {
    "device_type": "zerotier",
    "slug": "zerotier",
    "collected_at": "${collected_at}",
    "data": {
        "node_id": "${node_id}",
        "version": "${version}",
        "status": "${status}",
        "networks": networks,
        "peers_summary": {
            "total": len(peers),
            "controllers": len(controllers),
            "leaves_total": len(leaves),
            "leaves_online": len(online_leaves),
        },
        "peers": peers
    }
}
print(json.dumps(data, indent=2))
PYEOF
