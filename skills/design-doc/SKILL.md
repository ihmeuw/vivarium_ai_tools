---
name: design-doc
description: "Write a formal design document from an approved design. Use after brainstorming is complete and a design has been approved. Produces an RST design document following the team template with goals, requirements as user stories, performance implications, tasks, and time estimates."
compatibility: "Requires file write access. Designed for VS Code Copilot agents."
metadata:
  author: ihmeuw
  version: "0.1"
---

# Write Design Document

Transform an approved design into a formal RST design document following the
team template.

<HARD-GATE>
Do NOT begin writing until you have a design that has been explicitly approved
by the user. If no approved design exists in the conversation context, ask the
user to provide one or invoke the brainstorming skill first.
</HARD-GATE>

## Process

1. **Gather the approved design** — read the design from conversation context or
   a referenced file/memory
2. **Load the template** — read [assets/template.rst](assets/template.rst)
3. **Fill each section** — transform the approved design into the template
   structure, following the section guidelines below
4. **Self-review** — check for placeholders, contradictions, ambiguity, scope
5. **Write the file** — save to `~/design_docs/YYYY-MM-DD-<topic>-design.rst`
6. **User review gate** — ask the user to review before proceeding

## Section Guidelines

**Goals:** 2-5 bullet points. Concrete, measurable where possible. Derived from
the "purpose" and "success criteria" identified during brainstorming.

**Background and strategic fit:** Why this work matters now. What problem it
solves. How it fits into the broader roadmap. 1-3 paragraphs.

**Assumptions:** What must be true for this design to work. Include technical
assumptions (dependencies, platform requirements) and process assumptions
(team capacity, external dependencies).

**Requirements:** Express as user stories in the format: "As a <type of user>,
I want <goal> so that <reason>." Classify each as "Must have" or "Nice to have."
Requirements should trace back to the goals.

**Current state:** Only include if modifying existing behavior. Describe what
exists today and why it needs to change.

**User interaction and design:** How users (developers, modelers, etc.) will
interact with the new functionality. Include CLI commands, API surfaces, agent
invocation patterns, or workflow steps as appropriate.

**Performance Implications:** For framework/model changes, discuss runtime and
memory impact. For agent tooling, discuss token budget and context window
implications. State "No significant performance implications" if truly N/A —
do not delete the section.

**Questions:** Capture unresolved questions from brainstorming. If all questions
were resolved, note the key decisions made and their rationale.

**Not Doing:** Explicitly state what is out of scope. This prevents scope creep
and sets expectations. Pull from the YAGNI decisions made during brainstorming.

**Tasks:** Break the implementation into discrete engineering tasks. Each task
should be independently completable and reviewable. Include priority and rough
estimates.

**Time estimate:** Total elapsed time for one engineer. Distinguish between
head-down engineering time and total time including waiting (reviews, CI, etc.).

## Self-Review Checklist

After writing the document, review it for:

1. **Placeholder scan** — any ALL_CAPS placeholders, "TBD", "TODO", or template
   text remaining? Fix them.
2. **Internal consistency** — do sections contradict each other? Does the task
   list cover all requirements? Do requirements trace to goals?
3. **Scope check** — is this focused enough for a single implementation effort,
   or does it need decomposition?
4. **Ambiguity check** — could any requirement be interpreted two different ways?
   Pick one interpretation and make it explicit.

Fix any issues inline. No separate review pass needed.

## User Review Gate

After writing and self-reviewing the document, present it to the user:

> "Design document written to `<path>`. Please review it and let me know if you
> want to make any changes."

Wait for the user's response. If they request changes, make them and re-run the
self-review checklist. Only proceed once the user approves.

## Output

- **File format:** reStructuredText (.rst)
- **Location:** `~/design_docs/YYYY-MM-DD-<topic>-design.rst`
- **Template:** [assets/template.rst](assets/template.rst)
