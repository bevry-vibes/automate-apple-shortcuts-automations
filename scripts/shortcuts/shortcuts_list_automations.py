#!/usr/bin/env python3
"""shortcuts_list_automations.py — read the FULL automation list in order.

TIER 2 (SHORTCUTS APP): walks the main window's AXOutline via PyObjC and
prints every row's texts in on-screen order.

usage: python shortcuts_list_automations.py [outfile]
  rows print as: <n>|<title> § <interval>
  e.g.  12|At 12:55 am, daily § Every 5 minutes

App-specific facts:
  * the automation list is an AXOutline inside the main window; rows carry
    their title ("At H:MM<nbsp-ap>am, daily" — Apple uses U+202F narrow
    no-break space) and subtitle (the interval) as static texts
  * the list is VIRTUALIZED: AX can return offscreen rows and, after
    re-renders, stale/double-captured rows. Cross-check counts against the
    sidebar badge, and detect true duplicates by ADJACENT identical rows in
    the sorted list.

Requires PyObjC (pyobjc-framework-ApplicationServices).
"""
import subprocess
import sys

from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCopyAttributeValue,
)


def get(el, attr):
    try:
        err, val = AXUIElementCopyAttributeValue(el, attr, None)
        return None if err != 0 else val
    except Exception:
        return None


def find_outlines(el, found):
    if get(el, "AXRole") == "AXOutline":
        found.append(el)
        return
    for k in get(el, "AXChildren") or []:
        find_outlines(k, found)


def row_texts(row):
    texts = []
    stack = [row]
    while stack:
        e = stack.pop(0)
        if get(e, "AXRole") == "AXStaticText":
            v = get(e, "AXValue")
            if v:
                texts.append(str(v))
        for c in get(e, "AXChildren") or []:
            stack.append(c)
    return texts


def main():
    out = sys.stdout
    if len(sys.argv) > 1:
        out = open(sys.argv[1], "w")
    pid = int(subprocess.check_output(["pgrep", "-x", "Shortcuts"]).split()[0])
    app = AXUIElementCreateApplication(pid)
    outlines = []
    for w in get(app, "AXWindows") or []:
        find_outlines(w, outlines)
    if not outlines:
        print("no outline found (open the Automation view)", file=sys.stderr)
        sys.exit(1)
    for ol in outlines:
        rows = get(ol, "AXChildren") or []
        for n, r in enumerate(rows, 1):
            texts = row_texts(r)
            if texts:
                print(f"{n}|{' § '.join(texts)}", file=out)
    if out is not sys.stdout:
        out.close()


if __name__ == "__main__":
    main()