# scripts/

Helper scripts from the live session that mass-created 288 Apple
Shortcuts Automations (see [DESIGN.md](../DESIGN.md)). Packaged so you
don't have to re-engineer them.

**Provenance:** developed and proven on macOS 26.x (Apple Silicon),
August 2026, by Hermes Agent + GLM 5.3 Flash. Reconstructed from session
artifacts; paths and coordinates are parameterized — calibrate for your
machine (one calibration per unique control; see calibration notes).

## What is generic vs app-specific vs ours

| Tier | Location | Applies to |
|---|---|---|
| **1. Generic macOS GUI automation** | [generic/](./generic/) | any macOS app: AX tree dumps, focus readback, element-at-point, true CGEvent clicks, cursor calibration, full-tree text walks, local OCR |
| **2. Apple Shortcuts app scripting** | [shortcuts/](./shortcuts/) | the Shortcuts app's Automation wizard specifically: New-Automation flow, time picker, Run-Immediately radio, shortcut picker cards, deletion + confirm dialog, full-list reader + audit, Automation-view selection |
| **3. Our shortcuts (NOT included)** | referenced only | the four *target shortcuts* our automations invoke ("Every 5 minutes", "Every Quarter Hour", "Every Half Hour", "Every Hour") and their card-grid coordinates. We share the *mechanism*, not our personal shortcuts — bring your own and calibrate your grid |

Tier 2 scripts reference card positions that were calibrated on our
machine — treat them as examples and re-derive yours (one
user-parked-mouse calibration; `generic/cursor_position.js` +
`generic/ax_element_at_point.py`).

## Setup

```sh
# PyObjC environment (PEP 668 blocks system pip; use uv or a venv)
uv venv .venv && uv pip install pyobjc-framework-ApplicationServices
# OCR helper (optional but recommended — deterministic reads, no LLM)
swiftc -O scripts/generic/ocr_read.swift -o /tmp/ocr  # needs Xcode CLT; export SDKROOT=$(xcrun --show-sdk-path)
```

## Hard rules learned the hard way (see DESIGN.md for why)

1. Never click screenshot pixels as native coordinates (Retina ≈ 1.28×).
2. System Events `click at` presses SwiftUI *activation points*, not the
   coordinates you pass — it is not a coordinate click.
3. AXPress sets values, not keyboard focus — read `AXFocusedUIElement`
   after every keystroke.
4. `Return` presses the **default** button: it submits wizard forms AND
   cancels destructive confirm dialogs.
5. Bracket every automated run with visible `display dialog` START/FINISH
   alerts; re-activate the target app after the dialog steals focus.
6. Verify with AX values first, local OCR second, vision LLM last.