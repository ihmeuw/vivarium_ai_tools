---
description: "Run a thorough code review across maintainability, DRY, design, tests, and documentation."
argument-hint: "A pull request to review, or a description of the changes to review."
allowed-tools: Task
---

Invoke the `code_reviewer` agent via the Task tool with the following
as its prompt brief:

$ARGUMENTS

Surface the orchestrator's synthesized review to the user without
rewriting it.
