#!/usr/bin/env python3
"""
Import device info from a Synology NAS via its HTTP API (DSM 7+).
Outputs JSON to stdout; hand to Claude for wiki/systems/ page creation.

Usage:
    ./synology.py <host> <user> [--password PASSWORD] [--port PORT]
    ./synology.py 192.168.1.50 admin
    ./synology.py nas.local admin --port 5001

Password: prompted interactively if not passed (avoids shell history)

Authentication: DSM session cookie (SynoToken). No credentials stored.

Requirements: pip install requests
"""

import argparse
import getpass
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


class SynologyAPI:
    def __init__(self, host, port, verify_ssl=False):
        self.base = f"https://{host}:{port}/webapi"
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.syno_token = None

    def login(self, user, password):
        r = self.session.get(f"{self.base}/auth.cgi", params={
            "api": "SYNO.API.Auth",
            "version": "7",
            "method": "login",
            "account": user,
            "passwd": password,
            "session": "import_script",
            "format": "cookie",
        })
        r.raise_for_status()
        d = r.json()
        if not d.get("success"):
            raise RuntimeError(f"Login failed: {d.get('error', {}).get('code')}")
        self.syno_token = d["data"].get("synotoken") or d["data"].get("did")

    def get(self, api, method, version=1, **params):
        p = {"api": api, "version": version, "method": method, **params}
        if self.syno_token:
            p["SynoToken"] = self.syno_token
        r = self.session.get(f"{self.base}/entry.cgi", params=p)
        r.raise_for_status()
        d = r.json()
        if not d.get("success"):
            return {}
        return d.get("data", {})

    def logout(self):
        self.session.get(f"{self.base}/auth.cgi", params={
            "api": "SYNO.API.Auth", "version": "1", "method": "logout", "session": "import_script"
        })


def main():
    parser = argparse.ArgumentParser(description="Import Synology NAS inventory")
    parser.add_argument("host", help="NAS host or IP")
    parser.add_argument("user", help="DSM username")
    parser.add_argument("--password", default=os.getenv("SYNOLOGY_PASSWORD"))
    parser.add_argument("--port", default=5001, type=int)
    args = parser.parse_args()

    password = args.password or getpass.getpass(f"DSM password for {args.user}@{args.host}: ")
    collected_at = datetime.now(timezone.utc).isoformat()

    api = SynologyAPI(args.host, args.port)
    try:
        api.login(args.user, password)

        info = api.get("SYNO.DSM.Info", "getinfo", version=2)
        storage = api.get("SYNO.Storage.CGI.Storage", "load_info", version=1)
        shares = api.get("SYNO.FileStation.List", "list_share", version=2, additional="real_path,owner,time,perm,mount_point_type,volume_status")
        volumes = api.get("SYNO.Core.Storage.Volume", "list", version=1, additional="fs_type,status,size,usage")
        network = api.get("SYNO.Core.Network", "get", version=2)
        services = api.get("SYNO.Core.Package.Service", "list", version=2)
        packages = api.get("SYNO.Core.Package", "list", version=2, additional="description,status")

        slug = args.host.replace(".", "-").replace("_", "-")
        hostname = info.get("hostname", slug)
        slug = hostname.lower().replace(" ", "-")

        output = {
            "device_type": "synology",
            "slug": slug,
            "collected_at": collected_at,
            "data": {
                "hostname": hostname,
                "model": info.get("model"),
                "dsm_version": info.get("version_string"),
                "serial": info.get("serial"),
                "uptime_seconds": info.get("uptime"),
                "ram_mb": info.get("ram_size"),
                "cpu_vendor": info.get("cpu_vendor"),
                "cpu_family": info.get("cpu_family"),
                "network": network,
                "volumes": volumes.get("volumes", []) if isinstance(volumes, dict) else [],
                "shares": (shares.get("shares", []) if isinstance(shares, dict) else []),
                "packages": [
                    {"name": p.get("id"), "version": p.get("version"), "status": p.get("status")}
                    for p in (packages.get("packages", []) if isinstance(packages, dict) else [])
                ],
            }
        }
        print(json.dumps(output, indent=2))
    finally:
        api.logout()


if __name__ == "__main__":
    main()
