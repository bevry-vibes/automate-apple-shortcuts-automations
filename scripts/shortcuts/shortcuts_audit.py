#!/usr/bin/env python3
"""shortcuts_audit.py — full-grid audit of time-of-day automations.

TIER 2 (SHORTCUTS APP) + TIER 3 (our schedule): reads the full automation
list (via shortcuts_list_automations) and diffs it against an expected
5-minute grid.

usage: python shortcuts_audit.py [--interval-map every5|quarter|half|hour]

Default expected mapping (OURS — tier 3; edit for your own):
  :00 -> Every Hour | :15/:45 -> Every Quarter Hour
  :30 -> Every Half Hour | others -> Every 5 minutes
  (our 00:00 row is intentionally "Every Day" — a daily-reset automation)

Outputs: total rows, unique slots, duplicates (adjacency-based, since the
list is sorted), missing slots, and any interval mismatches.

Parsing notes baked in:
  * titles look like `At 12:00< U+202F>am, daily` (narrow no-break space)
  * rows pair as (title, interval) alternately in the AX text stream
"""
import re
import subprocess
import sys
from collections import Counter

SCRIPT_DIR = subprocess.run(
    ["dirname", sys.argv[0]], capture_output=True, text=True).stdout.strip()


def read_rows():
    r = subprocess.run(
        [sys.executable, f"{SCRIPT_DIR}/shortcuts_list_automations.py"],
        capture_output=True, text=True)
    rows = []
    for l in r.stdout.splitlines():
        parts = l.split("|", 1)
        if len(parts) < 2:
            continue
        parts = parts[1].split(" § ")
        if len(parts) >= 2 and parts[0].startswith("At "):
            m = re.match(
                r"At (\d{1,2}):(\d{2})[\u202f\s](am|pm), daily", parts[0])
            if m:
                h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3)
                h24 = h % 12 + (12 if ap == "pm" else 0)
                rows.append((h24, mi, parts[1]))
    return rows


def expected_interval(mi):
    if mi == 0:
        return "Every Hour"
    if mi in (15, 45):
        return "Every Quarter Hour"
    if mi == 30:
        return "Every Half Hour"
    return "Every 5 minutes"


def main():
    rows = read_rows()
    cnt = Counter((h, mi) for h, mi, _ in rows)
    dups = sorted(k for k, v in cnt.items() if v > 1)
    missing = []
    for mins in range(0, 24 * 60, 5):
        h24, mi = divmod(mins, 60)
        if cnt.get((h24, mi), 0) == 0:
            missing.append((h24, mi))
    wrong = [(h, mi, g) for h, mi, g in rows
             if g != expected_interval(mi) and not (h == 0 and mi == 0)]
    midnight = [g for h, mi, g in rows if (h, mi) == (0, 0)]
    print(f"total rows: {len(rows)}")
    print(f"unique slots: {len(cnt)} / 288")
    print(f"duplicates: {dups}")
    print(f"missing: {missing}")
    print(f"wrong intervals (excl 00:00): {wrong}")
    print(f"00:00 interval: {midnight}")


if __name__ == "__main__":
    main()