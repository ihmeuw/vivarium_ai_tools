---
description: Use the GitHub CLI (gh) for PR operations, issue management, and repository tasks. Use when creating PRs, checking CI status, or managing issues.
disable-model-invocation: true
allowed-tools: Bash(gh *)
---

## GitHub CLI

Common `gh` workflows for vivarium development.

### Pull Requests

```bash
# Create a PR
gh pr create --title "Description" --body "Details" --base main

# Check PR status and CI
gh pr status
gh pr checks

# View PR diff
gh pr diff

# Merge when ready
gh pr merge --squash --delete-branch
```

### Issues

```bash
# List assigned issues
gh issue list --assignee @me

# View issue details
gh issue view <number>

# Create issue
gh issue create --title "Title" --body "Body" --label "bug"
```

### Repository

```bash
# Clone with all remotes
gh repo clone ihmeuw/<repo>

# View recent releases
gh release list

# Check CI run status
gh run list --limit 5
gh run view <run-id>
```
