#!/usr/bin/env python3
"""shortcuts_delete_automation.py — delete one automation by exact row title.

TIER 2 (SHORTCUTS APP): AX-select the row, Cmd+Delete, then press the RED
Delete button in the confirm dialog BY NAME.

usage:
  python shortcuts_delete_automation.py "At 3:00$(printf '\\u202f')am, daily"   # dialog left open
  python shortcuts_delete_automation.py <title> --confirm-axpress              # press Delete via AX

App-specific facts (all proven the hard way):
  * selecting a row and pressing plain Delete OPENS THE EDITOR — the delete
    shortcut is Cmd+Delete (key code 51 + command)
  * the "Delete automation?" confirm dialog's DEFAULT button is Cancel —
    pressing Return CANCELS the deletion (this caused phantom extras)
  * the red Delete button IS AXPress-able (AppKit): select it by
    `description is "Delete"`, never by index
  * the list row is selected via AX set AXSelected=true (PyObjC)

Requires PyObjC. The title must match exactly, including Apple's U+202F
narrow no-break space between time and am/pm.
"""
import subprocess
import sys
import time

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


def find_outlines(el, found):
    if get(el, "AXRole") == "AXOutline":
        found.append(el)
        return
    for k in get(el, "AXChildren") or []:
        find_outlines(k, found)


def row_title(row):
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
    return texts[0] if texts else ""


def osa(script):
    return subprocess.run(["osascript", "-e", script],
                          capture_output=True, text=True)


def main():
    title = sys.argv[1]
    confirm = "--confirm" in sys.argv
    pid = int(subprocess.check_output(["pgrep", "-x", "Shortcuts"]).split()[0])
    app = AXUIElementCreateApplication(pid)
    outlines = []
    for w in get(app, "AXWindows") or []:
        find_outlines(w, outlines)
    if not outlines:
        print("FAIL: no outline (Automation view open?)")
        sys.exit(1)
    target = None
    for r in get(outlines[0], "AXChildren") or []:
        if row_title(r) == title:
            target = r
            break
    if target is None:
        print(f"FAIL: {title!r} not among visible rows")
        sys.exit(1)
    if AXUIElementSetAttributeValue(target, "AXSelected", True) != 0:
        print("FAIL: could not select row")
        sys.exit(1)
    osa('tell application "Shortcuts" to activate')
    time.sleep(0.8)
    osa('tell application "System Events" to key code 51 using {command down}')
    time.sleep(1.5)
    if confirm:
        pr = osa('tell application "System Events" to tell process "Shortcuts" '
                 'to perform action "AXPress" of (first button of sheet 1 of '
                 'window 1 whose description is "Delete")')
        time.sleep(2.0)
        print("pressed named Delete button")
    else:
        print("dialog may be open — press the red Delete (AXPress by name); "
              "NEVER Return (default = Cancel)")


if __name__ == "__main__":
    main()