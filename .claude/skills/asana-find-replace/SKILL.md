---
name: asana-find-replace
description: Bulk find-and-replace text across all tasks and subtasks in an Asana project. Use this whenever the user wants to rename a product, update a placeholder, or replace any text across an entire Asana project. Trigger on phrases like "replace [X] with [Y] in my project", "I duplicated a project and need to update the product name", "change all tasks that say [old name] to [new name]", "I created a project from a template and need to swap out the placeholder", "update the product name in every task", or any request to do a text swap or bulk rename across Asana tasks. Always use this skill for Asana find-and-replace workflows — even if the user just says "find X replace with Y" and mentions a project name.
---

# Asana Bulk Find & Replace

This skill replaces a string of text across every task and subtask in an Asana project — useful when duplicating a project from a template, cloning a product launch project, or correcting a name that appears throughout.

## What you need from the user

Confirm you have all three before starting:
1. **Project** — name or Asana URL (you'll resolve it to a GID)
2. **Find** — the exact text to search for
3. **Replace with** — the new text

If any are missing, ask upfront. Don't start the workflow until you have all three.

## Workflow

### Step 1 — Locate the project

Use `search_objects` with `resource_type: project` and the project name. If multiple results come back, list them and ask the user to confirm the right one before proceeding.

### Step 2 — Pull ALL tasks and subtasks directly from the project

> **Critical:** Never use `search_objects` or `search_tasks_preview` to find tasks — these tools only index a subset of tasks and will silently miss the majority. Always use `get_tasks` scoped to the project:

```
get_tasks(
  project="<project_gid>",
  limit=100,
  opt_fields="name,subtasks,subtasks.name,parent"
)
```

This returns every top-level task with its subtasks nested inline. Walk through the results and collect:
- Every parent task (GID + name)
- Every subtask in each parent's `subtasks` array (GID + name)

If `next_page` is returned, paginate until you have everything.

### Step 3 — Filter to matches and prepare replacements

Go through every collected task and subtask name. For each one where the find text appears, compute the new name by replacing all occurrences of the find string with the replace string. Build a list of `{task_gid, new_name}` pairs.

Before updating, tell the user how many matches you found (e.g., "Found 83 tasks containing 'Fig' — proceeding with updates").

If zero matches are found, stop and tell the user clearly. Don't proceed with empty updates.

### Step 4 — Update in batches of 10

Use `update_tasks` with a `tasks` array. Keep batches at 10 or fewer — larger batches time out.

Each item needs:
- `task`: the GID string
- `name`: the replacement name

Run batches sequentially. Keep a running count of successes and failures.

### Step 5 — Report results

Summarize: "Updated X tasks — Y succeeded, Z failed." If any failed, list them so the user can decide whether to retry.

## Edge cases

**Potential false positives** — Before updating, scan the match list for cases where the find string might appear in an unintended context (e.g., searching "Fig" would also match "Figma", a tool name in a different project context). If you spot any, flag them to the user before proceeding. You don't need to be exhaustive — just use judgment on obvious cases.

**Case sensitivity** — The match is case-sensitive by default. If the user seems to expect case-insensitive matching, confirm before proceeding.

**Multiple projects with the same name** — Show the full list and ask the user to confirm.

**Large projects** — If the project has hundreds of tasks, give the user a progress update partway through (e.g., after every 50 updates).

## What to avoid

- Using search tools to find tasks — always use `get_tasks` scoped to the project GID
- Batches larger than 10 in a single `update_tasks` call
- Updating tasks you're not certain belong to this project (subtasks are safe since you collected them from the project's own task list)
