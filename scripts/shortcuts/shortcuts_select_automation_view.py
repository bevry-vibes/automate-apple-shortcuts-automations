#!/usr/bin/env python3
"""shortcuts_select_automation_view.py — open the Automation view via AX.

TIER 2 (SHORTCUTS APP): selects the "Automation" row in the sidebar by
matching its static texts (title "Automation" + badge), so list scripts and
audits work even when the app opens on Gallery.

usage: python shortcuts_select_automation_view.py
Requires PyObjC (pyobjc-framework-ApplicationServices).
"""
import subprocess
import sys

from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCopyAttributeValue,
    AXUIElementSetAttributeValue,
)


def get(el, attr):
    try:
        err, val = AXUIElementCopyAttributeValue(el, attr, None)
        return None if err != 0 else val
    except Exception:
        return None


def texts_under(el):
    vals = []
    stack = [el]
    while stack:
        e = stack.pop(0)
        if get(e, "AXRole") == "AXStaticText":
            v = get(e, "AXValue")
            if v:
                vals.append(str(v))
        stack.extend(get(e, "AXChildren") or [])
    return vals


def main():
    pid = int(subprocess.check_output(["pgrep", "-x", "Shortcuts"]).split()[0])
    app = AXUIElementCreateApplication(pid)

    def walk(el):
        if get(el, "AXRole") in ("AXRow", "AXTableRow"):
            vals = texts_under(el)
            if vals and vals[0] == "Automation":
                err = AXUIElementSetAttributeValue(el, "AXSelected", True)
                print("sidebar Automation row selected" if err == 0
                      else f"select failed err={err}")
                return err == 0
        for k in get(el, "AXChildren") or []:
            if walk(k):
                return True
        return False

    done = False
    for w in get(app, "AXWindows") or []:
        done = walk(w)
        if done:
            break
    if not done:
        print("Automation sidebar row not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()