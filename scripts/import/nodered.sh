#!/usr/bin/env bash
# Import flow inventory and runtime info from a Node-RED instance via REST API.
# Outputs JSON to stdout; hand to Claude for wiki/systems/ page creation.
#
# Usage: ./nodered.sh <base_url> [api_key]
# Example: ./nodered.sh http://192.168.1.20:1880
#          ./nodered.sh http://nodered.local:1880 my-api-key
#
# API key: set in Node-RED settings.js under httpNodeAuth or adminAuth API tokens.
# If no key needed (local trusted network), omit it.

set -euo pipefail

BASE_URL="${1:?Usage: $0 <base_url> [api_key]}"
BASE_URL="${BASE_URL%/}"  # strip trailing slash
API_KEY="${2:-}"
collected_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

auth_header=""
[ -n "$API_KEY" ] && auth_header="-H 'Authorization: Bearer ${API_KEY}'"

curl_cmd() {
  if [ -n "$API_KEY" ]; then
    curl -sf -H "Authorization: Bearer ${API_KEY}" "$@"
  else
    curl -sf "$@"
  fi
}

version_json=$(curl_cmd "${BASE_URL}/red/modules" 2>/dev/null || echo "{}")
settings_json=$(curl_cmd "${BASE_URL}/settings" 2>/dev/null || echo "{}")
flows_json=$(curl_cmd "${BASE_URL}/flows" 2>/dev/null || echo "[]")
nodes_json=$(curl_cmd "${BASE_URL}/nodes" 2>/dev/null || echo "[]")

python3 - <<PYEOF
import json, sys
from collections import Counter

try:
    flows = json.loads("""${flows_json}""")
except Exception:
    flows = []

try:
    nodes_installed = json.loads("""${nodes_json}""")
except Exception:
    nodes_installed = []

try:
    settings = json.loads("""${settings_json}""")
except Exception:
    settings = {}

# Summarise flows
node_types = Counter(n.get("type") for n in flows if n.get("type") != "tab")
tabs = [n for n in flows if n.get("type") == "tab"]
subflows = [n for n in flows if n.get("type") == "subflow"]

# Installed palettes (non-core)
palettes = [
    {"name": m.get("name"), "version": m.get("version"), "local": m.get("local", False)}
    for m in nodes_installed
    if not m.get("name", "").startswith("@node-red/")
    and m.get("name") != "node-red"
]

data = {
    "device_type": "nodered",
    "slug": "nodered",
    "collected_at": "${collected_at}",
    "data": {
        "base_url": "${BASE_URL}",
        "settings": {
            "version": settings.get("version"),
            "httpNodeRoot": settings.get("httpNodeRoot"),
            "httpAdminRoot": settings.get("httpAdminRoot"),
            "flowFilePath": settings.get("flowFilePath"),
            "credentialSecret": "<redacted>" if settings.get("credentialSecret") else None,
        },
        "flows_summary": {
            "total_nodes": len(flows),
            "tabs": len(tabs),
            "subflows": len(subflows),
            "tab_names": [t.get("label") or t.get("id") for t in tabs],
            "top_node_types": dict(node_types.most_common(20)),
        },
        "installed_palettes": palettes,
    }
}
print(json.dumps(data, indent=2))
PYEOF
