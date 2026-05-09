---
description: "Trace a simulation regression across vivarium repositories to identify the behavioral change causing it."
argument-hint: "Describe the regression symptom, repos/branches involved, and any researcher hypotheses."
allowed-tools: Task
---

Invoke the `model_regression_debugger` agent via the Task tool with the
following as its prompt brief:

$ARGUMENTS

Surface the orchestrator's findings to the user without rewriting them.
The orchestrator scopes the problem, narrows the change boundary, fans
out diff analyzers and hypothesis testers, and reports back.

If the user has not provided enough information for the orchestrator
to scope the problem (symptom, repos involved, ref/date boundary), let
the orchestrator's Phase 1 dialog prompt for the missing details rather
than blocking the invocation.
