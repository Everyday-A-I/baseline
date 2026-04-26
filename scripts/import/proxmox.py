#!/usr/bin/env python3
"""
Import node and VM/CT inventory from a Proxmox VE host via its REST API.
Outputs JSON to stdout; hand to Claude for wiki/systems/ page creation.

Usage:
    ./proxmox.py <host> <user> [--tokenid TOKEN_ID] [--secret SECRET]
    ./proxmox.py 192.168.1.100 root@pam --tokenid mytoken --secret xxxxxxxx-xxxx-...

Authentication options (in priority order):
  1. --tokenid + --secret  (API token — recommended; create in PVE > Datacenter > API Tokens)
  2. PROXMOX_TOKEN_ID + PROXMOX_TOKEN_SECRET env vars
  3. --password / PROXMOX_PASSWORD  (username+password — uses ticket auth)

Requirements: pip install requests (urllib3 included)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


def get_ticket(session, base_url, user, password):
    r = session.post(f"{base_url}/access/ticket", data={"username": user, "password": password}, verify=False)
    r.raise_for_status()
    d = r.json()["data"]
    session.headers.update({"CSRFPreventionToken": d["CSRFPreventionToken"]})
    session.cookies.set("PVEAuthCookie", d["ticket"])


def get(session, base_url, path):
    r = session.get(f"{base_url}{path}", verify=False)
    r.raise_for_status()
    return r.json().get("data", [])


def main():
    parser = argparse.ArgumentParser(description="Import Proxmox VE inventory")
    parser.add_argument("host", help="Proxmox host or IP")
    parser.add_argument("user", help="PVE user, e.g. root@pam")
    parser.add_argument("--tokenid", default=os.getenv("PROXMOX_TOKEN_ID"))
    parser.add_argument("--secret", default=os.getenv("PROXMOX_TOKEN_SECRET"))
    parser.add_argument("--password", default=os.getenv("PROXMOX_PASSWORD"))
    parser.add_argument("--port", default=8006, type=int)
    args = parser.parse_args()

    base_url = f"https://{args.host}:{args.port}/api2/json"
    session = requests.Session()

    if args.tokenid and args.secret:
        session.headers["Authorization"] = f"PVEAPIToken={args.user}!{args.tokenid}={args.secret}"
    elif args.password:
        get_ticket(session, base_url, args.user, args.password)
    else:
        print("Error: provide --tokenid+--secret or --password (or env vars)", file=sys.stderr)
        sys.exit(1)

    collected_at = datetime.now(timezone.utc).isoformat()

    nodes = get(session, base_url, "/nodes")
    result_nodes = []

    for node in nodes:
        node_name = node["node"]
        status = get(session, base_url, f"/nodes/{node_name}/status")
        vms = get(session, base_url, f"/nodes/{node_name}/qemu")
        cts = get(session, base_url, f"/nodes/{node_name}/lxc")
        storage = get(session, base_url, f"/nodes/{node_name}/storage")
        network = get(session, base_url, f"/nodes/{node_name}/network")

        vm_list = []
        for vm in vms:
            vm_config = {}
            try:
                vm_config = get(session, base_url, f"/nodes/{node_name}/qemu/{vm['vmid']}/config")
            except Exception:
                pass
            vm_list.append({
                "vmid": vm.get("vmid"),
                "name": vm.get("name"),
                "status": vm.get("status"),
                "maxcpu": vm.get("maxcpu"),
                "maxmem_bytes": vm.get("maxmem"),
                "disk_bytes": vm.get("maxdisk"),
                "os_type": vm_config.get("ostype"),
                "description": vm_config.get("description", ""),
                "onboot": vm_config.get("onboot", False),
                "agent": vm_config.get("agent"),
            })

        ct_list = []
        for ct in cts:
            ct_list.append({
                "vmid": ct.get("vmid"),
                "name": ct.get("name"),
                "status": ct.get("status"),
                "cpus": ct.get("cpus"),
                "maxmem_bytes": ct.get("maxmem"),
                "disk_bytes": ct.get("maxdisk"),
                "ostype": ct.get("ostype"),
                "onboot": ct.get("onboot", False),
            })

        result_nodes.append({
            "node": node_name,
            "status": node.get("status"),
            "cpu_usage": status.get("cpu"),
            "memory": status.get("memory"),
            "uptime_seconds": status.get("uptime"),
            "kernel": status.get("kversion"),
            "pve_version": status.get("pveversion"),
            "vms": vm_list,
            "containers": ct_list,
            "storage": [{"id": s.get("storage"), "type": s.get("type"), "total": s.get("total"), "used": s.get("used"), "avail": s.get("avail"), "active": s.get("active")} for s in storage],
            "network_interfaces": [{"iface": n.get("iface"), "type": n.get("type"), "address": n.get("address"), "cidr": n.get("cidr"), "bridge_ports": n.get("bridge_ports")} for n in network],
        })

    slug = args.host.replace(".", "-")
    output = {
        "device_type": "proxmox",
        "slug": f"proxmox-{slug}",
        "collected_at": collected_at,
        "data": {
            "host": args.host,
            "nodes": result_nodes,
        }
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
