#!/usr/bin/env python3
"""
Import Tuya device inventory from local network scan (no cloud dependency).
Uses tinytuya to scan and fingerprint devices operating in local mode.
Outputs JSON to stdout; hand to Claude for wiki/systems/ page creation.

Usage:
    ./tuya.py [--network CIDR] [--timeout SECONDS]
    ./tuya.py                          # scans 192.168.1.0/24 by default
    ./tuya.py --network 10.0.0.0/24

Requirements:
    pip install tinytuya

Device keys: tinytuya scan can fingerprint device IDs without keys.
For full state polling you need device keys from the Tuya IoT Platform
or a prior tinytuya wizard run (~/.tinytuya.json).
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    import tinytuya
except ImportError:
    print("Error: 'tinytuya' not installed. Run: pip install tinytuya", file=sys.stderr)
    sys.exit(1)


def load_known_devices():
    """Load previously scanned device keys if available."""
    paths = [
        os.path.expanduser("~/.tinytuya.json"),
        "devices.json",
        os.path.join(os.path.dirname(__file__), "devices.json"),
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p) as f:
                    return json.load(f)
            except Exception:
                pass
    return []


def main():
    parser = argparse.ArgumentParser(description="Scan for Tuya devices on local network")
    parser.add_argument("--network", default=None, help="CIDR to scan, e.g. 192.168.1.0/24")
    parser.add_argument("--timeout", default=5, type=int, help="Scan timeout per device (seconds)")
    args = parser.parse_args()

    collected_at = datetime.now(timezone.utc).isoformat()
    known = load_known_devices()
    known_by_id = {d.get("id"): d for d in known if d.get("id")}

    print("Scanning for Tuya devices (this may take 10-30 seconds)...", file=sys.stderr)

    try:
        if args.network:
            scanner = tinytuya.scanner.Scanner(network=args.network, timeout=args.timeout)
        else:
            scanner = tinytuya.scanner.Scanner(timeout=args.timeout)
        raw_devices = scanner.scan()
    except AttributeError:
        # Older tinytuya API
        try:
            raw_devices = tinytuya.deviceScan(verbose=False, maxretry=2)
            if isinstance(raw_devices, dict):
                raw_devices = list(raw_devices.values())
        except Exception as e:
            print(f"Scan failed: {e}", file=sys.stderr)
            raw_devices = []

    devices = []
    for d in (raw_devices or []):
        if isinstance(d, dict):
            dev_id = d.get("gwId") or d.get("id") or ""
            known_info = known_by_id.get(dev_id, {})
            devices.append({
                "id": dev_id,
                "name": known_info.get("name") or d.get("name", "unknown"),
                "ip": d.get("ip"),
                "version": d.get("version"),
                "product_key": d.get("productKey") or d.get("product_key"),
                "active": d.get("active"),
                "ability": d.get("ability"),
                "key_known": dev_id in known_by_id,
                "category": known_info.get("category", "unknown"),
            })

    output = {
        "device_type": "tuya",
        "slug": "tuya-devices",
        "collected_at": collected_at,
        "data": {
            "devices_found": len(devices),
            "keys_available": sum(1 for d in devices if d["key_known"]),
            "devices": devices,
            "note": "Run 'python -m tinytuya wizard' to collect device keys for local control. Keys stored in ~/.tinytuya.json"
        }
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
