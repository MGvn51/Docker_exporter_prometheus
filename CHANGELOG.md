# Change log
All notable changes to this project will be documented in this file.

## [0.1.1] - 2022-01-14

### Added

### Changed
- CPU metrics unit changed to seconds from 1/100th of second
- Removed metrics `mem_swap`, `mem_memory_limit` and `mem_memsw_limit`

### Fixed
- Log level accidentally left fixed at debug
- Fixed blkio metrics not being exported
- Fixed typo for metric `mem_mapped_file`

## [0.1.0] - 2022-01-13
Initial release