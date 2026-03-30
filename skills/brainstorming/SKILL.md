---
name: brainstorming
description: "Brainstorm ideas into designs through collaborative dialogue. Use when starting any new feature, workflow, component, or system change. Explores user intent, requirements, trade-offs, and design before implementation. Produces an approved design ready for documentation."
compatibility: "Designed for VS Code Copilot agents. Read-only tools recommended."
metadata:
  author: ihmeuw
  version: "0.1"
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a
time to refine the idea. Once you understand what you're building, present the
design and get user approval.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project,
or take any implementation action until you have presented a design and the user
has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A config change, a single-function
utility, a new skill definition — all of them. "Simple" projects are where
unexamined assumptions cause the most wasted work. The design can be short (a
few sentences for truly simple projects), but you MUST present it and get
approval.

## Checklist

You MUST complete these steps in order:

1. **Explore project context** — check files, docs, recent commits, repo structure
2. **Assess scope** — if the request spans multiple independent subsystems, flag it and help decompose into sub-projects before detailed design
3. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
5. **Present design** — in sections scaled to their complexity, get user approval after each section
6. **Design approval** — get explicit user approval of the complete design before handing off

## The Process

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
- Before asking detailed questions, assess scope: if the request describes
  multiple independent subsystems, flag this immediately. Don't spend questions
  refining details of a project that needs to be decomposed first.
- If the project is too large for a single spec, help the user decompose into
  sub-projects: what are the independent pieces, how do they relate, what order
  should they be built? Then brainstorm the first sub-project through the normal
  design flow.
- For appropriately-scoped projects, ask questions one at a time to refine
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message — if a topic needs more exploration, break it
  into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Scale each section to its complexity: a few sentences if straightforward, up
  to 200-300 words if nuanced
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing strategy
- Be ready to go back and clarify if something doesn't make sense

**Design for isolation and clarity:**

- Break the system into smaller units that each have one clear purpose,
  communicate through well-defined interfaces, and can be understood and tested
  independently
- For each unit, you should be able to answer: what does it do, how do you use
  it, and what does it depend on?
- Smaller, well-bounded units are easier for agents to work with — they reason
  better about code they can hold in context at once

**Working in existing codebases:**

- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work, include targeted
  improvements as part of the design
- Don't propose unrelated refactoring. Stay focused on what serves the current goal.

**Multi-agent workflow considerations:**

When designing a feature that will be implemented via a multi-agent workflow,
explicitly reason about:

- Which agents are involved and what pattern applies (sequential, parallel
  fan-out, generator/critic, etc.)
- Where tool permission boundaries should be (read-only vs. write stages)
- Where handoff points are and what context each agent needs
- Whether sub-agents need isolation (worktrees, separate working directories)

See [references/multi-agent-patterns.md](references/multi-agent-patterns.md) for
the pattern catalog.

## After the Design

**Design approval gate:**

After presenting the complete design, ask for explicit approval:

> "Design complete. Does this look right, or do you want to adjust anything
> before we write it up as a formal document?"

Wait for the user's response. If they request changes, revise and re-present.
Only hand off once the user approves.

**Handoff:**

The terminal state of brainstorming is handing off to a design document writer.
Do NOT invoke any implementation skill. The ONLY next step after brainstorming
is writing a formal design document from the approved design.

## Key Principles

- **One question at a time** — Don't overwhelm with multiple questions
- **Multiple choice preferred** — Easier to answer than open-ended when possible
- **YAGNI ruthlessly** — Remove unnecessary features from all designs
- **Explore alternatives** — Always propose 2-3 approaches before settling
- **Incremental validation** — Present design, get approval before moving on
- **Be flexible** — Go back and clarify when something doesn't make sense
- **Scope aggressively** — A focused design that ships beats a comprehensive one that doesn't
