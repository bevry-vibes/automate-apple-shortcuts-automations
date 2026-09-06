#!/usr/bin/env python3
"""ax_element_at_point.py — identify the AX element at screen coordinates.

TIER 1 (GENERIC): works with any macOS app. Requires PyObjC:
    uv venv && uv pip install pyobjc-framework-ApplicationServices

usage: python ax_element_at_point.py X Y [ProcessName]

This is the tool that makes user-parked-mouse calibration useful: have the
user hover the target control, read the exact cursor position (see
cursor_position.js), then hit-test that point HERE to derive the element's
real selector/role/actions — and act through selectors or the keyboard
from then on. Modern PyObjC (12.x) returns AX out-params as tuples:
    err, element = AXUIElementCopyElementAtPosition(syswide, x, y, None)

Provenance: built during the 2026-08-30 Apple Shortcuts session, where it
revealed the time picker is ONE composite AXRadioButton whose description
is "Time of Day, Time picker" — hour/minute/AM-PM have no sub-elements.
"""
import sys

from ApplicationServices import (  # noqa: F401
    AXUIElementCreateApplication,
    AXUIElementCreateSystemWide,
    AXUIElementCopyElementAtPosition,
    AXUIElementCopyAttributeValue,
    AXUIElementCopyAttributeNames,
    AXUIElementCopyActionNames,
)


def get(el, attr):
    try:
        err, val = AXUIElementCopyAttributeValue(el, attr, None)
        return None if err != 0 else val
    except Exception:
        return None


def fmt_geo(val):
    try:
        if hasattr(val, "x") and hasattr(val, "y"):
            return f"({val.x:.0f},{val.y:.0f})"
        if hasattr(val, "width") and hasattr(val, "height"):
            return f"{val.width:.0f}x{val.height:.0f}"
    except Exception:
        pass
    return None


def describe(el, depth, max_depth):
    if el is None or depth > max_depth:
        return
    role = get(el, "AXRole")
    subrole = get(el, "AXSubrole")
    desc = get(el, "AXDescription")
    title = get(el, "AXTitle")
    val = get(el, "AXValue")
    foc = get(el, "AXFocused")
    pos = fmt_geo(get(el, "AXPosition"))
    size = fmt_geo(get(el, "AXSize"))
    line = "  " * depth + f"[{role}/{subrole}] desc={desc!r} title={title!r} val={val!r} foc={foc}"
    if pos and size:
        line += f" @{pos} {size}"
    print(line)
    if depth == 0:
        err, names = AXUIElementCopyAttributeNames(el, None)
        if err == 0:
            print("  " * depth + "ATTRS:", sorted(map(str, names or [])))
        err, acts = AXUIElementCopyActionNames(el, None)
        if err == 0:
            print("  " * depth + "ACTIONS:", [str(a) for a in (acts or [])])
    err, parent = AXUIElementCopyAttributeValue(el, "AXParent", None)
    if err == 0:
        describe(parent, depth + 1, max_depth)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    x, y = float(sys.argv[1]), float(sys.argv[2])
    sw = AXUIElementCreateSystemWide()
    err, el = AXUIElementCopyElementAtPosition(sw, x, y, None)
    print(f"hit-test({x},{y}) err={err}")
    if err != 0:
        sys.exit(1)
    if len(sys.argv) > 3:
        pid = int(sys.argv[3])
        app_el = AXUIElementCreateApplication(pid)
        app_pid = get(app_el, "AXPid") or "(unknown)"
        print(f"(element pid context requested: {pid})")
    describe(el, 0, 8)


if __name__ == "__main__":
    main()