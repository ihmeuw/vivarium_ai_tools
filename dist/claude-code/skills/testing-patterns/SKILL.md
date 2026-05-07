---
description: Run tests and debug test failures in vivarium projects using pytest. Use when running tests, debugging failures, or checking coverage.
allowed-tools: Bash(pytest *) Bash(python -m pytest *)
---

## Testing with pytest

Vivarium projects use pytest with common patterns.

### Running Tests

```bash
# Run all tests
pytest tests/

# Run a specific test file
pytest tests/framework/test_engine.py

# Run a specific test
pytest tests/framework/test_engine.py::test_simulation_step -x -v

# Run with coverage
pytest tests/ --cov=src/ --cov-report=term-missing

# Run only fast tests (skip slow-marked tests)
pytest tests/ -m "not slow"
```

### Common Fixtures

- `hdf_file` — temporary HDF store for data tests
- `SimulationContext` / `build_simulation_from_model_spec` — full sim setup
- Parametrized tests use `@pytest.mark.parametrize`

### Debugging Failures

1. Run the failing test in isolation with `-x -v --tb=long`
2. Check if it's an ordering issue: `pytest --randomly-seed=<seed>`
3. For data-dependent tests, verify input fixtures are generating expected shapes
4. For simulation tests, check component initialization order via `sim.get_value()`
