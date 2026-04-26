#!/usr/bin/env bash
# Import device info from a Raspberry Pi (or any Debian/Ubuntu SBC) via SSH.
# Outputs JSON to stdout; hand to Claude for wiki/systems/ page creation.
#
# Usage: ./raspberry-pi.sh <host> [user]
# Example: ./raspberry-pi.sh 192.168.1.10 pi
#          ./raspberry-pi.sh sbc.local

set -euo pipefail

HOST="${1:?Usage: $0 <host> [user]}"
USER="${2:-pi}"
SSH="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 ${USER}@${HOST}"
collected_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

hostname=$($SSH "hostname" 2>/dev/null || echo "unknown")
model=$($SSH "cat /proc/device-tree/model 2>/dev/null | tr -d '\0'" || echo "unknown")
os=$($SSH "cat /etc/os-release | grep PRETTY_NAME | cut -d'\"' -f2" 2>/dev/null || echo "unknown")
kernel=$($SSH "uname -r" 2>/dev/null || echo "unknown")
uptime_sec=$($SSH "cat /proc/uptime | awk '{print int(\$1)}'" 2>/dev/null || echo "0")
cpu_temp=$($SSH "cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null" || echo "0")
mem=$($SSH "free -m | awk 'NR==2{print \$2\" total, \"\$3\" used, \"\$4\" free\"}'" 2>/dev/null || echo "")
df=$($SSH "df -h --exclude-type=tmpfs --exclude-type=devtmpfs" 2>/dev/null || echo "")
ip_addrs=$($SSH "ip -br addr show" 2>/dev/null || echo "")

# Services (systemd only)
services=$($SSH "systemctl list-units --type=service --state=running --no-pager --no-legend 2>/dev/null | awk '{print \$1}'" || echo "")

# Docker containers if present
docker_ps=$($SSH "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' 2>/dev/null" || echo "")

# GPIO / HAT detection
hat=$($SSH "cat /proc/device-tree/hat/product 2>/dev/null | tr -d '\0'" || echo "none")
vcgencmd=$($SSH "vcgencmd measure_temp 2>/dev/null" || echo "")

slug=$(echo "$hostname" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
cpu_temp_c=$(echo "$cpu_temp" | python3 -c "import sys; v=sys.stdin.read().strip(); print(round(int(v)/1000,1) if v.isdigit() else 0)")

python3 - <<PYEOF
import json

data = {
    "device_type": "raspberry-pi",
    "slug": "${slug}",
    "collected_at": "${collected_at}",
    "data": {
        "hostname": "${hostname}",
        "model": "${model}",
        "os": "${os}",
        "kernel": "${kernel}",
        "uptime_seconds": ${uptime_sec},
        "cpu_temp_celsius": ${cpu_temp_c},
        "hat": "${hat}",
        "memory": "${mem}",
        "storage": """${df}""",
        "network": "${ip_addrs}",
        "running_services": [s for s in """${services}""".strip().splitlines() if s],
        "docker_containers": """${docker_ps}""",
        "vcgencmd": "${vcgencmd}"
    }
}
print(json.dumps(data, indent=2))
PYEOF
