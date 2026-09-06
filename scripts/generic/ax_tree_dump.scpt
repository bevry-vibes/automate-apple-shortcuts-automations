-- ax_tree_dump.scpt — recursively dump the AX tree of a process's front window
-- TIER 1 (GENERIC): works with any macOS app via System Events.
-- usage: osascript ax_tree_dump.scpt <ProcessName>
-- Notes:
--   * `log` output goes to stderr; run with 2>&1 to capture.
--   * Some roles expose no value/position; those print as missing/empty.
--   * AppleScript under System Events hits terminology clashes with some
--     class names (outline/row/scroll area) — this dump only uses generic
--     `UI elements`, which is safe everywhere.

on dumpEl(el, depth)
	tell application "System Events"
		set r to ""
		try
			set r to role of el
		end try
		set sr to ""
		try
			set sr to subrole of el
		end try
		set v to ""
		try
			set v to (value of el) as text
		end try
		set f to ""
		try
			set f to (focused of el) as text
		end try
		set p to ""
		try
			set p to (position of el) as text
		end try
		set z to ""
		try
			set z to (size of el) as text
		end try
		set pad to ""
		repeat depth times
			set pad to pad & " "
		end repeat
		log pad & "[" & r & ":" & sr & "] val=" & v & " foc=" & f & " @" & p & " " & z
		set kids to {}
		try
			set kids to UI elements of el
		end try
		repeat with k in kids
			my dumpEl(k, depth + 1)
		end repeat
	end tell
end dumpEl

on run argv
	set procName to item 1 of argv
	tell application "System Events"
		tell process procName
			my dumpEl(window 1, 0)
		end tell
	end tell
end run