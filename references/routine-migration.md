# Routine Migration Reference — Skills repo → SJ-OS

Generated to recreate all 23 scheduled Routines pointed at `SWEETJULY26/SJ-OS` (main) instead of the old standalone `SWEETJULY26/Skills` repo. Create each of these from the claude.ai Routines UI so MCP connectors attach correctly (the API path from this session can't pass connector grants to a new trigger).

For each Routine below: **delete the old one** (same name, still pointing at `Skills`) **and create a new one** with the same name, same cron schedule, same environment/connectors, but the updated prompt text.

---

## sjs-monthly-sop-sync

**Cron:** `0 16 1 * *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Microsoft_365, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-monthly-sop-sync' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-monthly-sop-sync.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## ac-brands-holiday-comms-2026

**Cron:** `0 16 * * 1`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Microsoft_365, mcp__Asana, mcp__Asana-c313a468

**Prompt:**
```
You are running scheduled task 'ac-brands-holiday-comms-2026' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/ac-brands-holiday-comms-2026.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-quality-quarterly-rollup

**Cron:** `30 14 1-3 1,4,7,10 *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468

**Prompt:**
```
You are running scheduled task 'sjs-quality-quarterly-rollup' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-quality-quarterly-rollup.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-quality-monthly-snapshot

**Cron:** `15 14 1-3 * *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468

**Prompt:**
```
You are running scheduled task 'sjs-quality-monthly-snapshot' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-quality-monthly-snapshot.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-quality-weekly-digest

**Cron:** `45 14 * * 1`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468

**Prompt:**
```
You are running scheduled task 'sjs-quality-weekly-digest' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-quality-weekly-digest.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-quality-morning-sweep

**Cron:** `20 15 * * 1-5`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Microsoft_365

**Prompt:**
```
You are running scheduled task 'sjs-quality-morning-sweep' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-quality-morning-sweep.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-purchasing-quarterly-rollup-and-snapshot

**Cron:** `20 14 1-3 1,4,7,10 *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-purchasing-quarterly-rollup-and-snapshot' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-purchasing-quarterly-rollup-and-snapshot.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-purchasing-monthly-rollup-and-snapshot

**Cron:** `10 14 1-3 * *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-purchasing-monthly-rollup-and-snapshot' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-purchasing-monthly-rollup-and-snapshot.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-purchasing-weekly-digest

**Cron:** `30 14 * * 1`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft-365, Supabase, Netlify, Fireflies, Vercel, Asana, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468

**Prompt:**
```
You are running scheduled task 'sjs-purchasing-weekly-digest' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-purchasing-weekly-digest.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-purchasing-morning-sweep

**Cron:** `26 15 * * 1-5`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Microsoft_365, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-purchasing-morning-sweep' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-purchasing-morning-sweep.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-monthly-sop-run

**Cron:** `0 14 8-14 * 4`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-monthly-sop-run' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-monthly-sop-run.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-regulatory-quarterly-cost-rollup

**Cron:** `5 14 1-3 1,4,7,10 *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-regulatory-quarterly-cost-rollup' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-regulatory-quarterly-cost-rollup.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-regulatory-monthly-rollup-and-snapshot

**Cron:** `0 14 1-3 * *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-regulatory-monthly-rollup-and-snapshot' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-regulatory-monthly-rollup-and-snapshot.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-regulatory-weekly-digest

**Cron:** `15 14 * * 1`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-regulatory-weekly-digest' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-regulatory-weekly-digest.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-regulatory-morning-sweep

**Cron:** `10 15 * * 1-5`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Microsoft_365, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-regulatory-morning-sweep' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-regulatory-morning-sweep.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-marketing-research--weekly-run

**Cron:** `40 15 * * 1`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, WebSearch

**Prompt:**
```
You are running scheduled task 'sjs-marketing-research--weekly-run' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-marketing-research--weekly-run.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## ayesha-weekly-briefing-friday

**Cron:** `0 15 * * 5`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Microsoft_365, mcp__Fireflies, mcp__Supabase, mcp__Canva

**Prompt:**
```
You are running scheduled task 'ayesha-weekly-briefing-friday' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/ayesha-weekly-briefing-friday.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## pd-quarterly-rollup

**Cron:** `45 14 1-3 1,4,7,10 *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'pd-quarterly-rollup' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/pd-quarterly-rollup.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## pd-monthly-rollup

**Cron:** `20 14 1-3 * *`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'pd-monthly-rollup' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/pd-monthly-rollup.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## weekly-pd-update

**Cron:** `0 15 * * 1`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft-365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'weekly-pd-update' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/weekly-pd-update.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-pd-eod-reconciliation

**Cron:** `0 23 * * 1-5`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-pd-eod-reconciliation' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-pd-eod-reconciliation.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-pd-midday-sweep

**Cron:** `0 19 * * 1-5`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft_365, Supabase, Netlify, Excalidraw, Fireflies, Vercel, Asana, Canva, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Microsoft_365, mcp__Fireflies, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-pd-midday-sweep' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-pd-midday-sweep.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---

## sjs-pd-morning-sweep

**Cron:** `50 14 * * 1-5`  
**Model:** `claude-sonnet-4-6`  
**Connectors:** Microsoft-365, Supabase, Netlify, Fireflies, Vercel, Asana, Asana-c313a468  
**Allowed tools:** Bash, Read, Glob, Grep, mcp__Asana, mcp__Asana-c313a468, mcp__Microsoft_365, mcp__Fireflies, mcp__Supabase

**Prompt:**
```
You are running scheduled task 'sjs-pd-morning-sweep' as a remote routine. Work in America/Los_Angeles time.

STEP 1 — clone the skills+prompts repo (sanitize the token from any output):
  git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/SWEETJULY26/SJ-OS.git" /home/user/sj-os 2>&1 | sed -E 's#x-access-token:[^@]+@#x-access-token:***@#g'
If the clone fails, STOP and report the sanitized error.

STEP 2 — read /home/user/sj-os/scheduled-prompts/sjs-pd-morning-sweep.md and follow it EXACTLY. Read every skill file it lists from /home/user/sj-os/.claude/skills/<name>/SKILL.md and follow those as instructions (they are plain files, not auto-registered skills).

Use the attached MCP connectors for all external systems; never reference local mcp tool ids. Read HUB_FUNCTION_SECRET from the environment when publishing to landing-hub. Do not write any local files. Begin.
```

---
