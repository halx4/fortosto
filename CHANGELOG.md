# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed

## [1.0.0] - 2021-05-10

### Added

 - basic support for importing json lines (.jsonl) files
 - shorthand argument `-die`, an alias of `--drop-if-exists`

### Changed

 - (breaking change) changed the default file pattern from '*.csv' to '*.*'
 - improved compatibility with capital letters on table,schema and column names

### Fixed

## [0.1.3] - 2021-04-26

### Fixed
 - bug where application is crashing when a single file is the target

## [0.1.2] - 2021-04-25

### Added

### Changed

### Removed

### Fixed

[unreleased]: https://github.com/halx4/fortosto/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/halx4/fortosto/releases/tag/v1.0.0
[0.1.3]: https://github.com/halx4/fortosto/releases/tag/v0.1.3
[0.1.2]: https://github.com/halx4/fortosto/releases/tag/v0.1.2
