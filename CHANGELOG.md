# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0]

### Added
- Custom formatter validation functions: `validate_file_formatter()` and `validate_directory_formatter()`
  - Validates formatter callability, parameter count, return type, and output safety
  - Prevents invalid formatters that could produce unsafe filenames (path separators, null bytes)
  - Provides clear error messages for invalid formatters
- Comprehensive test suite for formatter validation

### Changed
- Improved docstrings for `unused_filename()` and `unused_directory()` with clearer examples and better parameter descriptions
- Enhanced README documentation with improved examples and usage patterns

## [1.0.0]

### Added
- Initial release of unused-path Python package
- `unused_filename()` function to generate unused file paths by auto-incrementing numeric suffixes
- `unused_directory()` function to generate unused directory paths by auto-incrementing numeric suffixes
- Support for custom formatters to customize the numbering format
- Atomic file and directory creation with `create=True` option (race-safe)
- Intelligent handling of existing numbered files/directories (continues sequence)
- Helper functions: `parse_suffix()`, `try_create_file()`, `try_create_directory()`, `make_full_path()`
- Default formatters: `default_file_formatter()`, `default_directory_formatter()`
- Type hints for better IDE support and type checking
- Zero dependencies for minimal overhead
- Comprehensive test suite with unit tests, integration tests, and race condition tests
- Python 3.8+ compatibility

### Features
- Automatically appends numeric suffixes to avoid filename conflicts
- Similar behavior to how browsers handle duplicate downloads
- Handles gaps in numbered sequences intelligently
- Supports custom formatting patterns

[1.1.0]: https://github.com/ysskrishna/unused-path/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ysskrishna/unused-path/releases/tag/v1.0.0
