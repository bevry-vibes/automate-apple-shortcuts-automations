-- ax_focus_readback.scpt — print role/description/value of the focused element
-- TIER 1 (GENERIC): any process.
-- usage: osascript ax_focus_readback.scpt <ProcessName>
--
-- Read this after EVERY synthetic keystroke: keystrokes that "didn't take"
-- are almost always focus sitting somewhere you didn't expect.

on run argv
	set procName to item 1 of argv
	tell application "System Events"
		tell process procName
			set f to value of attribute "AXFocusedUIElement"
			set r to ""
			set d to ""
			set v to ""
			try
				set r to role of f
			end try
			try
				set d to description of f
			end try
			try
				set v to (value of f) as text
			end try
			return "role=" & r & " desc=" & d & " val=" & v
		end tell
	end tell
end run