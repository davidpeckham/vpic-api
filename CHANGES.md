# Change Log

## [0.7.1] - 2021-06-19

### Fixed
- WMI.common_name and other properties are no longer required

## [0.7.0] - 2021-06-17

### Changed
- Renamed WorldManufacturerIndex as WMI

## [0.6.3] - 2021-06-01

### Fixed
- My github profile URL

## [0.6.2] - 2021-06-01

### Added
- py.typed

### Removed
- Hard-coded version string. If you used this, you can get the same version string from importlib.metdata (Python 3.8+) or importlib_metadata (Python 3.7).

### Fixed
- Desert is now a runtime dependency, not a dev dependency

## [0.6.1] - 2021-05-31

### Fixed
- Typo in CHANGES.md

## [0.6.0] - 2021-05-31

### Added
- Support for vPIC Version 3.6, which was released on 2021-05-29
- Support for vPIC Version 3.5, which was release on 2021-05-14

## [0.3.1] - 2021-05-14

### Fixed
- Fixed property names in README.md and in TypedClient docstrings

## [0.3.0] - 2021-05-14

### Added
- Dataclasses for API return types
- TypedClient returns dataclasses instead of JSON
- Unit tests for TypedClient

## [0.2.0] - 2021-05-09

### Added
- Added mypi.ini

### Changed
- Renamed vpic.Vpic to vpic.Client
- Updated unit test expected results to use standardized variable names so they don't require patching (#5).
- Updated README.md with a code example

## [0.1.1] - 2021-05-05

### Changed
- Reclassified responses and six as dev dependencies
- Added repo URL to pyproject.toml
- Tests are now only included in the source distribution

## [0.1.0] - 2021-05-05

Initial release