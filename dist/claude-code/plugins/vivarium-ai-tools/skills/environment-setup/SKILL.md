---
description: Create and manage Python environments for vivarium projects using conda or venv. Use when setting up a new project, resolving dependency issues, or creating development environments.
disable-model-invocation: true
allowed-tools: Bash(conda *) Bash(pip *) Bash(python -m venv *)
---

## Environment Setup

Create a development environment for a vivarium project.

### Steps

1. Check if `pyproject.toml` exists in the project root
2. Determine environment type from project configuration:
   - If `environment.yml` exists → use conda
   - Otherwise → use python venv
3. Create the environment:
   - **conda**: `conda create -n <project-name> python=3.11 -y && conda activate <project-name>`
   - **venv**: `python -m venv .venv && source .venv/bin/activate`
4. Install the project in development mode: `pip install -e ".[dev]"`
5. Verify: `python -c "import <package_name>; print(<package_name>.__version__)"`

### Common Issues

- If `pip install -e .` fails with resolver conflicts, try: `pip install -e . --no-deps` then install deps individually
- For vivarium projects, always install with `[dev]` extras to get test dependencies
- Check `python_versions.json` for supported Python versions
