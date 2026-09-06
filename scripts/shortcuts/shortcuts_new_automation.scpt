-- shortcuts_new_automation.scpt — create ONE time-of-day automation in Apple
-- Shortcuts, end to end.
-- TIER 2 (SHORTCUTS APP): drives the Automation wizard specifically.
-- usage: osascript shortcuts_new_automation.scpt <HH> <MM> <am|p> <cardX> <cardY>
--
-- Calibration needed (one-time, user-parked mouse + ax_element_at_point.py):
--   * HOUR_FIELD_X/Y — the time picker's hour segment (SwiftUI composite;
--     CGEvent click REQUIRED — AXPress/Tab/arrows/click-at all fail)
--   * CARD_X/CARD_Y — your interval card in the picker grid (passed in)
--
-- App-specific facts baked in here (proven macOS 26.x, Aug 2026):
--   * ⌥⌘N = File > New Automation (never click the + button)
--   * ↓ once + Enter selects "Time of Day" in the trigger sheet
--   * Enter SUBMITS the When form (default button = Next) and later DONE
--   * Run Immediately = radio button 2 of the 2-radio AXRadioGroup; AXPress
--     works (AppKit-backed radio) — verify by re-reading its value == 1
--   * footer wizard buttons ignore AXPress (SwiftUI) — use Enter
--   * sheet fingerprints: When-sheet title "When"; picker title "At <time>, daily"

on sheetExists()
	tell application "System Events"
		tell process "Shortcuts"
			try
				set x to sheet 1 of window 1
				return true
			on error
				return false
			end try
		end tell
	end tell
end sheetExists

on clickAt(x, y)
	-- true CGEvent click; see generic/real_click.py for the standalone version
	do shell script "/usr/bin/env python3 -c \"import Quartz,time; e=Quartz.CGEventCreateMouseEvent(None,Quartz.kCGEventMouseMoved,(" & x & "," & y & "),Quartz.kCGMouseButtonLeft); Quartz.CGEventPost(0,e); time.sleep(0.12); e=Quartz.CGEventCreateMouseEvent(None,Quartz.kCGEventLeftMouseDown,(" & x & "," & y & "),Quartz.kCGMouseButtonLeft); Quartz.CGEventPost(0,e); time.sleep(0.08); e=Quartz.CGEventCreateMouseEvent(None,Quartz.kCGEventLeftMouseUp,(" & x & "," & y & "),Quartz.kCGMouseButtonLeft); Quartz.CGEventPost(0,e)\""
end clickAt

on run argv
	set hh to item 1 of argv
	set mm to item 2 of argv
	set apKey to item 3 of argv -- "a" or "p"
	set cardX to item 4 of argv
	set cardY to item 5 of argv
	set hourX to item 6 of argv
	set hourY to item 7 of argv

	display dialog "START: creating automation " & hh & ":" & mm & ". Hands off until FINISH." giving up after 3
	delay 0.5
	tell application "Shortcuts" to activate
	delay 1.2
	tell application "System Events"
		if not (frontmost of process "Shortcuts") then return "FAIL: Shortcuts not frontmost"
		if my sheetExists() then
			key code 53 -- Escape once if a stale sheet lingers
			delay 0.6
			if my sheetExists() then return "FAIL: stale sheet"
		end if
		keystroke "n" using {command down, option down} -- New Automation
		delay 1.5
		key code 125 -- Down: Time of Day
		delay 0.8
		key code 36 -- Enter: open When sheet
		delay 1.5
		if not my sheetExists() then return "FAIL: no When sheet"
		-- time: click hour segment, type, RIGHT between segments
		my clickAt(hourX, hourY)
		delay 0.8
		keystroke hh
		delay 0.7
		key code 124
		delay 0.7
		keystroke mm
		delay 0.7
		key code 124
		delay 0.7
		keystroke apKey
		delay 0.7
		-- Run Immediately via AXPress on the 2-radio group
		tell process "Shortcuts"
			set sa to scroll area 1 of group 1 of sheet 1 of window 1
			set rgs to radio groups of sa
			repeat with g in rgs
				if (count of radio buttons of g) is 2 then
					perform action "AXPress" of radio button 2 of g
					exit repeat
				end if
			end repeat
		end tell
		delay 1
		key code 36 -- Enter: submit When form -> picker
		delay 1.8
		if not my sheetExists() then return "FAIL: no picker sheet"
		my clickAt(cardX, cardY) -- your interval card (calibrate!)
		delay 1.5
		key code 36 -- Enter: Done
		delay 1.5
		if my sheetExists() then
			key code 53
			return "WARN: sheet stuck, escaped (verify nothing was created)"
		end if
	end tell
	display dialog "FINISH: automation " & hh & ":" & mm & " created." giving up after 2
	return "OK"
end run