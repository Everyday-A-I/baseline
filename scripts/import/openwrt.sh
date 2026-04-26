#!/usr/bin/env bash
# Import device info from an OpenWrt router via SSH.
# Outputs JSON to stdout; redirect to a file and hand to Claude for wiki page creation.
#
# Usage: ./openwrt.sh <host> [user]
# Example: ./openwrt.sh 192.168.1.1
#          ./openwrt.sh 192.168.1.1 root
#
# Requirements: ssh access to the router (key-based recommended)

set -euo pipefail

HOST="${1:?Usage: $0 <host> [user]}"
USER="${2:-root}"
SSH="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 ${USER}@${HOST}"

collected_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

board=$($SSH "cat /proc/cpuinfo | grep 'machine' | cut -d: -f2 | xargs" 2>/dev/null || echo "")
if [ -z "$board" ]; then
  board=$($SSH "cat /tmp/sysinfo/board_name 2>/dev/null" || echo "unknown")
fi
model=$($SSH "cat /tmp/sysinfo/model 2>/dev/null" || echo "unknown")
openwrt_release=$($SSH "cat /etc/openwrt_release" 2>/dev/null || echo "")
hostname=$($SSH "uci get system.@system[0].hostname 2>/dev/null" || echo "unknown")
uptime_sec=$($SSH "cat /proc/uptime | awk '{print int(\$1)}'" 2>/dev/null || echo "0")
kernel=$($SSH "uname -r" 2>/dev/null || echo "unknown")

# Network interfaces
interfaces=$($SSH "ip -j addr show 2>/dev/null || ip addr show" 2>/dev/null | head -100)

# UCI network config (sanitised — no passwords)
uci_network=$($SSH "uci export network 2>/dev/null" | grep -v -E 'password|secret|key|token' || echo "")
uci_wireless=$($SSH "uci export wireless 2>/dev/null" | grep -v -E 'key|password|secret' || echo "")
uci_dhcp=$($SSH "uci export dhcp 2>/dev/null" | grep -v -E 'password|secret' || echo "")
uci_mwan3=$($SSH "uci export mwan3 2>/dev/null" | grep -v -E 'password|secret' || echo "") 2>/dev/null || uci_mwan3=""

# Installed packages (abridged — count + key packages)
pkg_count=$($SSH "opkg list-installed 2>/dev/null | wc -l" || echo "0")
key_pkgs=$($SSH "opkg list-installed 2>/dev/null | grep -E 'mwan3|zerotier|wireguard|sing-box|dnscrypt|stubby|banip|adblock|statistics|prometheus|luci'" || echo "")

# Storage
df=$($SSH "df -h" 2>/dev/null || echo "")

# Derive a slug from hostname
slug=$(echo "$hostname" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')

python3 - <<PYEOF
import json, sys

data = {
    "device_type": "openwrt",
    "slug": "${slug}",
    "collected_at": "${collected_at}",
    "data": {
        "hostname": "${hostname}",
        "model": "${model}",
        "board": "${board}",
        "kernel": "${kernel}",
        "uptime_seconds": ${uptime_sec},
        "openwrt_release": """${openwrt_release}""",
        "network": {
            "uci_network": """${uci_network}""",
            "uci_wireless": """${uci_wireless}""",
            "uci_dhcp": """${uci_dhcp}""",
            "uci_mwan3": """${uci_mwan3}""",
            "interfaces_raw": """${interfaces}"""
        },
        "packages": {
            "installed_count": ${pkg_count},
            "key_packages": """${key_pkgs}"""
        },
        "storage": """${df}"""
    }
}
print(json.dumps(data, indent=2))
PYEOF
