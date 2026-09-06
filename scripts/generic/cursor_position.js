// cursor_position.js — print the current mouse position in native screen coords
// TIER 1 (GENERIC): macOS. Run with: osascript -l JavaScript cursor_position.js
//
// Calibration flow: ask the user to PARK their mouse over the target control,
// run this, and use the printed coordinates as ground truth — feed them to
// ax_element_at_point.py to derive the element selector.
//
// Gotcha: JXA cannot read AXUIElementCopyElementAtPosition out-params (returns
// undefined) — that's why the hit-test lives in Python, not here.

ObjC.import('CoreGraphics');

function main() {
    const loc = $.CGEventGetLocation($.CGEventCreate(null));
    return JSON.stringify({ x: loc.x, y: loc.y });
}
main()