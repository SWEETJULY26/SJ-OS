# Skill Audit Checklist

A static pass for reviewing an existing skill against Claude Code best practices — separate from the eval loop. Use it when someone wants a skill checked for quality without running test cases, or as a pre-flight before you start the eval/iterate loop on a skill someone else wrote.

Read the skill's SKILL.md and its bundled files first. Never propose changes to a skill you haven't read. Fix what you find before calling the audit done, and explain *why* each fix matters rather than just flipping a box — the reasoning is what makes the skill better, not the checkmark.

For any field or pattern referenced below, the full details live in [skill-reference.md](skill-reference.md).

## Frontmatter

- `name` matches the directory name; lowercase, hyphens, max 64 chars.
- `description` uses the words someone would actually say when they need this skill, and leans slightly "pushy" to fight under-triggering (see the description guidance in SKILL.md).
- `description` is specific enough to avoid false triggers but broad enough to catch real requests — the near-miss cases are where this usually breaks.
- `disable-model-invocation: true` is set if the skill has side effects (writes files, calls paid APIs, sends messages). Auto-invocation on a skill that spends money or sends mail is a real hazard.
- `argument-hint` is set if the skill takes arguments via `/name`.
- `allowed-tools` is set if the skill should not reach every tool — narrow it to what the workflow needs.
- `context: fork` (plus `agent`) is used only when the skill is self-contained and doesn't need conversation history. A fork that only carries guidelines with no concrete task returns nothing useful.
- `model` is set only when a specific capability tier is actually needed.
- No field is set just because it exists. Every line of frontmatter should earn its place.

## Content

- SKILL.md is under ~500 lines; heavy detail has moved to `references/`.
- The workflow is concrete — each step tells the model what to do and why, not a vague gesture.
- Output format is pinned down with a template or example where the output shape matters.
- File paths (inputs, outputs, scripts, references) are spelled out, not left implicit.
- Subagent delegation includes the actual prompt text to send, not "delegate this."
- Edge cases, hard constraints, and "do not do X" boundaries are stated — framed as reasoning, not a wall of capitalized MUSTs.
- String substitutions (`$ARGUMENTS`, `$N`) appear wherever the skill takes input.

## Integration

- Supporting files are referenced from SKILL.md, not orphaned in the directory.
- Bundled scripts have correct paths and run.
- Secrets and API keys live in environment variables, never hardcoded in skill files.
- The skill doesn't duplicate what already lives in CLAUDE.md or another skill. If an instruction should always apply, it belongs in CLAUDE.md, not here.
- Optionally, the skill is noted in the project's CLAUDE.md so the team knows it exists.

## Quality

- Someone without prior context could follow it.
- Instructions are actionable, not abstract.
- It delegates to subagents where that keeps the main context clean.
- Output paths follow a predictable convention.

After the audit, scan [skill-reference.md](skill-reference.md) for features that could sharpen the skill — `context: fork`, `allowed-tools`, dynamic context injection, hooks, bundled scripts. If the skill has objectively checkable outputs, the natural next step is to leave the static audit behind and run the eval/iterate loop in SKILL.md.
