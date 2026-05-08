---
description: Run standard Makefile targets for vivarium projects. Use when building, testing, linting, or formatting code.
allowed-tools: Bash(make *)
---

## Make Commands

Vivarium projects use a standard Makefile with these targets:

### Available Targets

| Target | Purpose |
|--------|---------|
| `make build` | Build the project (install deps, compile assets) |
| `make test` | Run the full test suite |
| `make lint` | Run linters (ruff, mypy) |
| `make format` | Auto-format code (ruff format, isort) |
| `make check` | Run lint + test (CI equivalent) |
| `make clean` | Remove build artifacts |
| `make docs` | Build documentation |

### Usage Notes

- Always run `make format` before committing
- `make check` is what CI runs — use it to verify before pushing
- Some projects have `make integration` for slow/cluster tests
- Check the project's `Makefile` for additional project-specific targets
