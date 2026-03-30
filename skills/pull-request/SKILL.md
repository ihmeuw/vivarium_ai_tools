---
name: pull-request
description: "Create a pull request using the target repo's PR template and the gh CLI. Use when changes are committed and ready for review. Reads .github/pull_request_template.md from the repo, fills template fields, and runs gh pr create."
compatibility: "Requires gh CLI authenticated. Requires git with committed changes on a feature branch."
metadata:
  author: ihmeuw
  version: "0.1"
---

# Create Pull Request

Create a well-formatted pull request using the target repo's PR template and
the `gh` CLI.

## Prerequisites

Before invoking this skill:
- Changes must be committed to a feature branch (not main/master)
- The branch must be pushed to the remote (or will be pushed by `gh`)
- The `gh` CLI must be installed and authenticated

## Process

1. **Identify the target repo** — determine which repo the PR is for from
   the current working directory or user context
2. **Read the PR template** — load `.github/pull_request_template.md` from
   the target repo. If no template exists, use the default structure from
   [references/default-template.md](references/default-template.md)
3. **Determine the PR title** — summarize the changes in imperative mood,
   starting with an upper case letter, no trailing period, ideally ≤50 chars
4. **Fill the template** — populate each section based on the changes made
   and conversation context. See section guidelines below.
5. **Confirm with user** — present the filled PR title and body for review
   before creating
6. **Create the PR** — run `gh pr create` with the filled template

## Section Guidelines

These guidelines match the standard vivarium PR template. Adapt if the repo's
template differs.

**Title:** Imperative mood summary. ≤50 characters ideal. Examples:
- "Add brainstorming and design-doc skills"
- "Fix race condition in artifact caching"

**Description:**
- *Category*: one of `bugfix`, `documentation`, `revert`, `other/misc`
- *JIRA issue*: link to the JIRA ticket, or "N/A" if none

**Changes and notes:** Explain what changed and why. Include:
- What the PR does (high-level summary)
- Why (motivation, context)
- Anything non-obvious or that needs reviewer attention
- If changes are complex, provide guidance on review order

**Testing:** How the changes were verified. Include:
- Unit tests added or modified
- Manual testing performed
- Integration testing for framework changes
- "Manual validation of skill/agent invocation" is acceptable for
  agent plugin changes

## Creating the PR

Use `gh pr create` with explicit title and body:

```bash
gh pr create \
  --title "<title>" \
  --body "<filled template body>" \
  --base main
```

If the branch hasn't been pushed yet, `gh` will offer to push it. Accept.

If the repo has a default base branch other than `main`, detect it with
`gh repo view --json defaultBranchRef`.

## Common Categories

- Agent/skill additions or changes → `other/misc`
- Bug fixes → `bugfix`
- README, changelog, docstring updates → `documentation`
- Reverting a previous change → `revert`
