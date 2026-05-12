# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `generate_spec` option on `setup_aiohttp_apispec` / `AiohttpApiSpec` to disable OpenAPI spec generation while keeping `validation_middleware` working. Defaults to the `APIGAMI_GENERATE_SPEC` env var (truthy `1`/`true`/`yes`/`on`, falsy `0`/`false`/`no`/`off`, case-insensitive), falling back to enabled. When disabled, route scanning, spec building, the spec endpoint, and Swagger UI mount are all skipped. Resolves [#110](https://github.com/anna-money/aiohttp-apigami/issues/110) ([#111](https://github.com/kulapard/aiohttp-apigami/pull/111)).

### Changed

- Updated Swagger UI to v5.32.5 ([#102](https://github.com/kulapard/aiohttp-apigami/pull/102), [#103](https://github.com/kulapard/aiohttp-apigami/pull/103), [#109](https://github.com/kulapard/aiohttp-apigami/pull/109)).
- Bumped `codecov/codecov-action` from 5 to 6 ([#104](https://github.com/kulapard/aiohttp-apigami/pull/104)).
- Bumped `pypa/gh-action-pypi-publish` from 1.13.0 to 1.14.0 ([#106](https://github.com/kulapard/aiohttp-apigami/pull/106)).
