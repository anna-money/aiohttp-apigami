# Add explicit option to disable OpenAPI spec generation

## Overview

Add user-friendly way to disable OpenAPI spec generation in aiohttp-apigami. Controlled via `generate_spec` parameter on `setup_aiohttp_apispec` / `AiohttpApiSpec`, with `APIGAMI_GENERATE_SPEC` environment variable as fallback default. When disabled, skip route scanning, spec building, swagger endpoint, and Swagger UI mounting — keep parser registration so `validation_middleware` still works.

Resolves anna-money/aiohttp-apigami#110.

## Context

- Files involved:
  - `aiohttp_apigami/core.py` — `AiohttpApiSpec.__init__`, `register`, `_register`, `setup_aiohttp_apispec`
  - `aiohttp_apigami/__init__.py` — re-exports (no public symbol change expected)
  - `tests/test_register.py` — register tests, add disabled cases
  - `README.md` — document new option
- Related patterns:
  - Boolean kwargs on `setup_aiohttp_apispec` (e.g. `in_place`)
  - `validation_middleware` depends on `app[APISPEC_PARSER]` + `app[APISPEC_VALIDATED_DATA_NAME]` set in `register`
  - Issue workaround patches `_register` to skip on every startup (~22ms savings per test)
- Dependencies: stdlib `os` for env var read

## Development Approach

- Testing approach: Regular (code first, then tests)
- Complete each task fully before moving to next
- Backwards-compatible default: `generate_spec=True`
- Env var name: `APIGAMI_GENERATE_SPEC` (truthy `1`/`true`/`yes`/`on` case-insensitive → enable; falsy `0`/`false`/`no`/`off` → disable; invalid → default `True`). Param value, when explicitly passed, overrides env var.
- CRITICAL: every task MUST include new/updated tests
- CRITICAL: all tests must pass before starting next task

## Implementation Steps

### Task 1: Add `generate_spec` flag and disable path in core

**Files:**
- Modify: `aiohttp_apigami/core.py`
- Modify: `tests/test_register.py`

- [x] Add `_ENV_VAR = "APIGAMI_GENERATE_SPEC"` constant and helper `_resolve_generate_spec(generate_spec: bool | None) -> bool` — returns `generate_spec` if not None, else parses env var (truthy/falsy strings), defaults to `True` when unset or invalid
- [x] Add `generate_spec: bool | None = None` kwarg to `AiohttpApiSpec.__init__`; add `_generate_spec` to `__slots__` and store resolved value
- [x] In `register()`: always set `app[APISPEC_VALIDATED_DATA_NAME]`, `app[APISPEC_PARSER]`, and `parser.error_callback` (so `validation_middleware` works); when `self._generate_spec is False`, skip `_register` / `_register_on_startup`, skip `_setup_spec_endpoint`, skip swagger UI setup; set `self._registered = True` and return
- [x] Add `generate_spec: bool | None = None` kwarg to `setup_aiohttp_apispec` and forward to `AiohttpApiSpec`
- [x] Update docstring on `setup_aiohttp_apispec` to document `generate_spec` semantics and `APIGAMI_GENERATE_SPEC` env var fallback
- [x] Write tests in `tests/test_register.py`:
  - `generate_spec=False` skips swagger spec route and `SWAGGER_DICT` population
  - `generate_spec=False` still configures `APISPEC_PARSER` + `APISPEC_VALIDATED_DATA_NAME` so middleware works
  - `generate_spec=False` + `swagger_path` does not register Swagger UI routes
  - Default (`generate_spec=None`, env unset) behaves identically to current behavior
- [x] Run project test suite — must pass before task 2

### Task 2: Env var fallback support

**Files:**
- Modify: `tests/test_register.py`

- [x] Confirm `_resolve_generate_spec` reads env var only when param is `None`; explicit `generate_spec=True` or `generate_spec=False` always wins
- [x] Add tests using `monkeypatch.setenv`:
  - `APIGAMI_GENERATE_SPEC=0` disables when param omitted
  - `APIGAMI_GENERATE_SPEC=false` disables (case-insensitive)
  - `APIGAMI_GENERATE_SPEC=1` enables (same as default)
  - Explicit `generate_spec=True` overrides `APIGAMI_GENERATE_SPEC=0`
  - Invalid env value (e.g. `maybe`) falls back to default `True`
- [x] Run test suite — must pass before task 3

### Task 3: Documentation

**Files:**
- Modify: `README.md`

- [x] Add short section near "Setup Function" / quickstart describing `generate_spec` parameter and `APIGAMI_GENERATE_SPEC` env var, with testing example replacing the `patch("AiohttpApiSpec._register")` workaround from the issue
- [x] Run test suite — must pass before task 4

### Task 4: Verify acceptance criteria

- [x] Run full test suite (`make test` or `pytest`)
- [x] Run linter (`make lint` or configured pre-commit)
- [x] Verify coverage on new branches in `core.py` exercised (target 80%+ overall, 100% on new code paths)

### Task 5: Finalize

- [x] Update `CLAUDE.md` if internal patterns changed (skipped — no `CLAUDE.md` in repo)
- [x] Move this plan to `docs/plans/completed/`
