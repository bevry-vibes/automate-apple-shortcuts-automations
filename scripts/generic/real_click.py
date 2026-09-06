#!/usr/bin/env python3
"""real_click.py — post a TRUE mouse click via CGEvent at native coordinates.

TIER 1 (GENERIC): works on any app, including SwiftUI internals that ignore
AXPress and ignore System Events' `click at` (which presses the element's
activation point instead of the given coordinates — do not use it as a
coordinate click).

usage: python real_click.py X Y [DOUBLE]

Requires PyObjC (pyobjc-framework-ApplicationServices). Accessibility (and on
modern macOS, Screen Recording for some targets) permission required for the
hosting terminal/process.

Provenance: this exact mechanism was the ONLY thing that could (a) focus the
Apple Shortcuts time picker's hour segment for typing, and (b) press the
shortcut picker's card grid — both SwiftUI internals.
"""
import sys
import time

import Quartz


def post(event_type, x, y, clicks=1):
    ev = Quartz.CGEventCreateMouseEvent(
        None, event_type, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventSetIntegerValueField(
        ev, Quartz.kCGMouseEventClickState, clicks)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)


def main():
    x, y = float(sys.argv[1]), float(sys.argv[2])
    clicks = 2 if len(sys.argv) > 3 and sys.argv[3] == "DOUBLE" else 1
    post(Quartz.kCGEventMouseMoved, x, y)
    time.sleep(0.12)
    for _ in range(clicks):
        post(Quartz.kCGEventLeftMouseDown, x, y)
        time.sleep(0.08)
        post(Quartz.kCGEventLeftMouseUp, x, y)
        time.sleep(0.12)
    print(f"posted {clicks} click(s) at ({x},{y})")


if __name__ == "__main__":
    main()