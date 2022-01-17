# Change log
All notable changes to this project will be documented in this file.

## [0.2.1] - 2022-01-17

### Added

### Changed

### Fixed
- Fixed `cpu_user_seconds` and `cpu_system_seconds` not being reported in seconds
- Fixed formatting for Metrics_exported.md

## [0.2.0] - 2022-01-17

### Added
- Added ability to choose between minimal, standard and extended levels of metrics using `METRICS_DETAILS` as an environment variable
- Added minimal metrics similar to `docker stats` command (~10.5% faster than standard)
- Added extended metrics, this will report the largest amount of informations (~4.5% slower than standard)
- Added environment variable `CONTAINERS_RELOAD_SECONDS` to choose when to reload the docker containers (to update state)
- Added metric for how long it took to update the containers metrics

### Changed

### Fixed
- Fixed cpu metrics not finishing in `_seconds` and not having a `_` between the prefix and the rest of the metric
- Fixed error where `METRICS_PREFIX` was not being used instead of the default one
- Fixed wrong function name causing the container to crash if some of the environment variables were invalid

## [0.1.1] - 2022-01-14

### Added

### Changed
- CPU metrics unit changed to seconds from 1/100th of second
- Removed metrics `mem_swap`, `mem_memory_limit` and `mem_memsw_limit`

### Fixed
- Log level accidentally left fixed at debug
- Fixed blkio metrics not being exported
- Fixed typo for metric `mem_mepped_file`

## [0.1.0] - 2022-01-13
Initial release