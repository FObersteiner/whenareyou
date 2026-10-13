# Changelog

<https://keepachangelog.com/>

Types of changes

- 'Added' for new features.
- 'Changed' for changes in existing functionality.
- 'Deprecated' for soon-to-be removed features.
- 'Removed' for now removed features.
- 'Fixed' for any bug fixes.
- 'Security' in case of vulnerabilities.

## [Unreleased]

## v0.8.0, 2026-10-13

### Changed

- bump Python dependency to 3.10
- look up IATA codes via a dict (O(1)) instead of scanning a list
- add a 10s timeout to Nominatim requests

### Fixed

- send a `User-Agent` header so Nominatim no longer returns HTTP 403
- parse `airports.csv` with `csv.DictReader` (quoted commas corrupted ~859 rows)
- `whenareyou_IATA` no longer rejects valid codes at index 0 (e.g. `AAA`)
- raise `ValueError` on network/HTTP errors instead of leaking `URLError`
- correct `_cached_get`/`_queryOSM` return type annotations

## v0.7.2, 2025-01-12

### Changed

- move package management from poetry to uv

## v0.7.1, 2024-09-03

### Changed

- cleanup code

### Removed

- drop dependency: requests; use urllib directly

## v0.7.0, 2024-03

### Changed

- update dependencies

### Removed

- Python 3.8 support

## v0.6.1, 2023-08

### Added

- type hints

### Changed

- update tests, 'Brussels, Europe' is not recognized by nominatim anymore

## v0.6.0, 2023-03

### Removed

- Python 3.7 support
