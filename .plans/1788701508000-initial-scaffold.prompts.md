# Prompts: initial project scaffold

Companion to [1788701508000-initial-scaffold.md](./1788701508000-initial-scaffold.md).
Prompts verbatim, in order, as delivered to the agent. Timestamps: only session-start observed (Sun Sep 6 2026, AWST, UTC+08:00); later prompts arrived mid-session without observable clock times, so none are fabricated.

**Agent model:** GLM 5.3 Flash (via ollama-cloud), harness: Hermes Agent (desktop)
**Session start:** Sunday, September 06, 2026 (AWST)

---

## Prompt 1

> Fantastic work GLM 5.3 Flash. We'll setup a open-source project for this at @url:`https://github.com/bevry-vibes/automate-apple-shortcuts-automations` which I've given the description `Used Hermes with GLM 5.3 Flash to automate mass creation of Automations within Apple Shortcuts` - follow the instructions at @url:`https://github.com/bevry-vibes/skills` to scaffold the project. We want to publish our our plan to .plans and note all our design learnings, nifties, innovations at DESIGN.md and how to use it for end users with Hermes and GLM 5.3 Flash in the README.md

(Agent note: attached context included a GitHub 404 page for the target repo URL at fetch time and the bevry-vibes/skills README listing policy/license/conventions/plans/commits skills.)

## Prompt 2 (followup, after consent block on npx agent-detect)

> Yeah, agent-detevt is already built, refer to ~/Projects/vibes/agent-detect use that one for detection, as you already added your detection to it there.

## Prompt 3 (mid-work steering, delivered during file setup)

> Make your project dir in ~/Projects/vibes/

## Session context (pre-prompts)

The project documents a completed live session (same harness+model, earlier on 2026-08-30) that mass-created 288 Apple Shortcuts automations via GUI automation — 69 existed (00:00–05:40), 219 were created, 5 duplicates deleted, 1 wrong-interval automation (23:30) fixed; verified 288/288 slots, 0 dups/gaps. That session's learnings are distilled into DESIGN.md; its raw working skill lives in the user's local Hermes skills (`shortcuts-bulk-automations`).

## Post-steering

None yet — plan is being committed at scaffold time.