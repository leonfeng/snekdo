---
name: context-compile
description: >-
  Compile reachability-based Python code context before implementing an OpenSpec
  task. Use when applying changes to snekdo with a known .py edit target.
---

# Context compile

Compile tiered Python context with [context-compiler](https://github.com/Emmimal/context-compiler) before editing code during OpenSpec apply.

## When to use

- **Do** call `context-compile` at the start of a Python implementation task when the task names or clearly implies a single edit target (e.g. `snekdo/api.py`, `tests/test_cli.py`).
- **Do** still read OpenSpec artifacts (`proposal.md`, delta specs, `design.md`, `tasks.md`) in full via normal reads — this tool replaces broad code exploration, not spec context.
- **Skip** during explore, propose, archive, or when the task is exploratory with no clear `.py` target.
- **Skip** for non-Python files (templates, config, docs).

## How to use

1. Identify the primary Python file for the current task.
2. Call the `context-compile` tool with `target_file` set to a repo-relative path.
3. Use the returned tier-1 full source and tier-2 skeletons as your code context.
4. If diagnostics flag dynamic-dispatch blind spots, read those files explicitly with the read tool.

## Defaults

- `max_hops`: 2 (direct imports plus one layer out)
- Implementation lives in `tools/context-compiler/`; wrapper CLI is `tools/context_compile.py`

## OpenSpec apply integration

During `/opsx-apply` or `openspec-apply-change`, after reading `contextFiles` and before the first implementation write for a Python task:

1. Call `context-compile` on the task's primary `.py` file.
2. Implement from that compiled context plus the OpenSpec artifacts already read.
3. Do not re-run `context-compile` for the same target unless imports changed materially.
