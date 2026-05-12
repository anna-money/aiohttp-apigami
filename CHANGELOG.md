# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `generate_spec` option on `setup_aiohttp_apispec` / `AiohttpApiSpec` to disable OpenAPI spec generation while keeping `validation_middleware` working. Defaults to the `APIGAMI_GENERATE_SPEC` env var (truthy `1`/`true`/`yes`/`on`, falsy `0`/`false`/`no`/`off`, case-insensitive), falling back to enabled. When disabled, route scanning, spec building, the spec endpoint, and Swagger UI mount are all skipped. Resolves [#110](https://github.com/anna-money/aiohttp-apigami/issues/110) ([#111](https://github.com/anna-money/aiohttp-apigami/pull/111)).

### Changed

- Updated Swagger UI to v5.32.5 ([#102](https://github.com/anna-money/aiohttp-apigami/pull/102), [#103](https://github.com/anna-money/aiohttp-apigami/pull/103), [#109](https://github.com/anna-money/aiohttp-apigami/pull/109)).
- Bumped `codecov/codecov-action` from 5 to 6 ([#104](https://github.com/anna-money/aiohttp-apigami/pull/104)).
- Bumped `pypa/gh-action-pypi-publish` from 1.13.0 to 1.14.0 ([#106](https://github.com/anna-money/aiohttp-apigami/pull/106)).

## [0.6.0] - 2026-02-13

### Added

- Support for generic type aliases in schema resolution ([#94](https://github.com/anna-money/aiohttp-apigami/pull/94)).
- Test for generic dataclass with nested custom dataclass ([#96](https://github.com/anna-money/aiohttp-apigami/pull/96)).

### Changed

- Updated Swagger UI to the latest 5.31.x version ([#85](https://github.com/anna-money/aiohttp-apigami/pull/85), [#90](https://github.com/anna-money/aiohttp-apigami/pull/90), [#93](https://github.com/anna-money/aiohttp-apigami/pull/93)).
- Bumped `actions/checkout` from 5 to 6 ([#88](https://github.com/anna-money/aiohttp-apigami/pull/88)).
- Bumped `peter-evans/create-pull-request` from 7 to 8 ([#92](https://github.com/anna-money/aiohttp-apigami/pull/92)).
- Refreshed multiple pre-commit hooks via pre-commit.ci ([#86](https://github.com/anna-money/aiohttp-apigami/pull/86), [#87](https://github.com/anna-money/aiohttp-apigami/pull/87), [#89](https://github.com/anna-money/aiohttp-apigami/pull/89), [#91](https://github.com/anna-money/aiohttp-apigami/pull/91), [#97](https://github.com/anna-money/aiohttp-apigami/pull/97)).

### Fixed

- Prevent spurious "Multiple schemas provided" warnings when handling falsy data ([#99](https://github.com/anna-money/aiohttp-apigami/pull/99)).

## [0.5.7] - 2025-11-05

### Added

- Python 3.14 support and weekly scheduled CI workflow ([#84](https://github.com/anna-money/aiohttp-apigami/pull/84)).

### Changed

- Updated Swagger UI to v5.30.1 ([#83](https://github.com/anna-money/aiohttp-apigami/pull/83)).
- Bumped `actions/checkout` from 4 to 5 ([#69](https://github.com/anna-money/aiohttp-apigami/pull/69)).
- Bumped `astral-sh/setup-uv` from 6 to 7 ([#80](https://github.com/anna-money/aiohttp-apigami/pull/80)).
- Bumped `pypa/gh-action-pypi-publish` from 1.12.4 to 1.13.0 ([#75](https://github.com/anna-money/aiohttp-apigami/pull/75)).
- pre-commit autoupdate ([#72](https://github.com/anna-money/aiohttp-apigami/pull/72)).

## [0.5.6] - 2025-06-21

### Changed

- Updated Swagger UI to v5.24.1 ([#54](https://github.com/anna-money/aiohttp-apigami/pull/54), [#59](https://github.com/anna-money/aiohttp-apigami/pull/59), [#60](https://github.com/anna-money/aiohttp-apigami/pull/60)).
- Bumped `astral-sh/setup-uv` from 5 to 6 ([#56](https://github.com/anna-money/aiohttp-apigami/pull/56)).
- pre-commit autoupdate ([#55](https://github.com/anna-money/aiohttp-apigami/pull/55), [#57](https://github.com/anna-money/aiohttp-apigami/pull/57)).

## [0.5.5] - 2025-04-07

### Changed

- Updated Swagger UI to v5.20.7 ([#53](https://github.com/anna-money/aiohttp-apigami/pull/53)).
- pre-commit autoupdate ([#52](https://github.com/anna-money/aiohttp-apigami/pull/52)).

## [0.5.4] - 2025-04-07

### Added

- Swagger UI tests ([#48](https://github.com/anna-money/aiohttp-apigami/pull/48)).

### Changed

- Made `marshmallow-recipe` an optional dependency ([#49](https://github.com/anna-money/aiohttp-apigami/pull/49)).

## [0.5.3] - 2025-03-28

### Changed

- Refactored test fixtures ([#46](https://github.com/anna-money/aiohttp-apigami/pull/46)).
- Increased test coverage ([#47](https://github.com/anna-money/aiohttp-apigami/pull/47)).

## [0.5.2] - 2025-03-27

### Changed

- Refactored `ApigamiPlugin` ([#44](https://github.com/anna-money/aiohttp-apigami/pull/44)).

## [0.5.1] - 2025-03-26

### Fixed

- `requestBody` for OpenAPI v3 ([#42](https://github.com/anna-money/aiohttp-apigami/pull/42)).

### Changed

- Process `aiohttp` routes via a plugin ([#42](https://github.com/anna-money/aiohttp-apigami/pull/42)).
- pre-commit autoupdate ([#40](https://github.com/anna-money/aiohttp-apigami/pull/40)).

## [0.5.0] - 2025-03-23

### Added

- `dataclass` support for request and response schemas ([#34](https://github.com/anna-money/aiohttp-apigami/pull/34)).
- Restored `setup_aiohttp_apispec` for backward compatibility with `aiohttp-apispec` ([#38](https://github.com/anna-money/aiohttp-apigami/pull/38)).

### Changed

- Renamed package `apispec-aiohttp` → `aiohttp-apigami` ([#37](https://github.com/anna-money/aiohttp-apigami/pull/37)).
- Refactored OpenAPI handling with version-specific processors ([#36](https://github.com/anna-money/aiohttp-apigami/pull/36)).
- Updated decorator docstrings with relevant examples ([#35](https://github.com/anna-money/aiohttp-apigami/pull/35)).

## [0.4.3] - 2025-03-21

### Changed

- Refactored README ([#33](https://github.com/anna-money/aiohttp-apigami/pull/33)).

## [0.4.2] - 2025-03-21

### Changed

- Refactored constants ([#31](https://github.com/anna-money/aiohttp-apigami/pull/31)).
- Used a unique prefix for all app keys (`web.AppKey`) ([#32](https://github.com/anna-money/aiohttp-apigami/pull/32)).

## [0.4.1] - 2025-03-21

### Added

- `layout` option for Swagger UI configuration ([#28](https://github.com/anna-money/aiohttp-apigami/pull/28)).

## [0.4.0] - 2025-03-21

### Changed

- Refactored code architecture with improved modularization ([#27](https://github.com/anna-money/aiohttp-apigami/pull/27)).

## [0.3.1] - 2025-03-17

### Added

- Script to update Swagger UI ([#21](https://github.com/anna-money/aiohttp-apigami/pull/21)).
- GitHub workflow to automate Swagger UI version updates ([#22](https://github.com/anna-money/aiohttp-apigami/pull/22)).

### Fixed

- Swagger UI update workflow ([#23](https://github.com/anna-money/aiohttp-apigami/pull/23)).

## [0.3.0] - 2025-03-17

### Changed

- Updated `aiohttp` minimum version and improved type hints ([#13](https://github.com/anna-money/aiohttp-apigami/pull/13), [#18](https://github.com/anna-money/aiohttp-apigami/pull/18)).
- Replaced MIT License with Apache License 2.0 ([#19](https://github.com/anna-money/aiohttp-apigami/pull/19), [#20](https://github.com/anna-money/aiohttp-apigami/pull/20)).
- CI: enabled caching for `uv` setup ([#14](https://github.com/anna-money/aiohttp-apigami/pull/14)); install pip for mypy ([#15](https://github.com/anna-money/aiohttp-apigami/pull/15)).
- Formatted docstrings ([#16](https://github.com/anna-money/aiohttp-apigami/pull/16)).

## [0.2.1] - 2025-03-16

### Added

- Class-based view in example app ([#11](https://github.com/anna-money/aiohttp-apigami/pull/11)).

### Changed

- Use `uv` instead of `pip` in dependabot ([#10](https://github.com/anna-money/aiohttp-apigami/pull/10)).
- Replaced `issubclass_py37fix` with `is_class_based_view` ([#12](https://github.com/anna-money/aiohttp-apigami/pull/12)).

## [0.2.0] - 2025-03-13

### Changed

- Replaced Jinja2 with `string.Template` for `index.html` rendering ([#9](https://github.com/anna-money/aiohttp-apigami/pull/9)).

## [0.1.4] - 2025-03-13

### Fixed

- Removed `use_kwargs` from `__all__` ([#8](https://github.com/anna-money/aiohttp-apigami/pull/8)).

## [0.1.3] - 2025-03-12

### Changed

- Replaced `**kwargs: Any` with properly typed parameters in `@docs` ([#6](https://github.com/anna-money/aiohttp-apigami/pull/6)).

## [0.1.2] - 2025-03-12

### Changed

- Removed unused mypy config ([#2](https://github.com/anna-money/aiohttp-apigami/pull/2)).
- Refactored to use `AppKey` instead of strings ([#3](https://github.com/anna-money/aiohttp-apigami/pull/3)).
- Refactored request handling to use `HandlerSchema` ([#4](https://github.com/anna-money/aiohttp-apigami/pull/4)).

## [0.1.1] - 2025-03-12

### Changed

- Updated Swagger UI static to v5.20.1 ([#1](https://github.com/anna-money/aiohttp-apigami/pull/1)).

## [0.1.0] - 2025-03-12

- First release.
