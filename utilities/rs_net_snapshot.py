#!/usr/bin/env python3

import json
import psutil

snapshot_file = "/tmp/rscontrol_net_stats.json"
snapshot = {}
for iface, stats in psutil.net_io_counters(pernic=True).items():
    snapshot[iface] = {
        "sent": stats.bytes_sent,
        "recv": stats.bytes_recv
    }

with open(snapshot_file, "w") as f:
    json.dump(snapshot, f)
