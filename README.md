# unused-path

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ysskrishna/unused-path/blob/main/LICENSE)
![Tests](https://github.com/ysskrishna/unused-path/actions/workflows/test.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/unused-path)](https://pypi.org/project/unused-path/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/unused-path?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/unused-path)

Generate unused file and directory paths by auto-incrementing numeric suffixes. Similar to how browsers handle duplicate downloads.

## Features

- **Automatic numbering**: Appends numeric suffixes like "file (1).txt", "file (2).txt" to avoid conflicts
- **Intelligent sequencing**: Continues from existing numbered files/directories
- **Custom formatting**: Support for custom formatter functions
- **Zero dependencies**: Lightweight with no external dependencies
- **Type safe**: Full type hints for excellent IDE support
- **Robust**: Handles edge cases, gaps in sequences, and special characters

## Installation

```bash
pip install unused-path
```

## Usage Examples

### Basic Usage

```python
from unused_path import unused_filename, unused_directory

# Generate unused filename
path = unused_filename("document.pdf")
print(path)  # 'document.pdf' (if available)

# If file exists, automatically increments
path = unused_filename("document.pdf")
print(path)  # 'document (1).pdf'

# Same for directories
dir_path = unused_directory("backup")
print(dir_path)  # 'backup' or 'backup (1)' if exists
```

### Atomic Creation (Race-Safe)

```python
# Atomically create file if it doesn't exist
path = unused_filename("download.zip", create=True)
# File is created atomically, safe for concurrent access

# Same for directories
dir_path = unused_directory("exports", create=True)
```

### Custom Formatting

```python
# Custom formatter for files
formatter = lambda base, ext, n: f"{base}_v{n:03d}{ext}"
path = unused_filename("log.txt", formatter=formatter)
print(path)  # 'log_v001.txt'

# Custom formatter for directories
formatter = lambda base, n: f"{base}_v{n}"
dir_path = unused_directory("backup", formatter=formatter)
print(dir_path)  # 'backup_v1'
```

### Handling Existing Numbered Files

```python
# If you have: test.txt, test (1).txt, test (3).txt
# The function will intelligently use test (2).txt
path = unused_filename("test.txt")
print(path)  # 'test (2).txt'
```

## API Reference

| Function | Description |
|----------|-------------|
| `unused_filename(path, *, formatter=None, max_tries=10000, create=False)` | Generate unused filename by appending numeric suffix if needed |
| `unused_directory(path, *, formatter=None, max_tries=10000, create=False)` | Generate unused directory name by appending numeric suffix if needed |

### Parameters

- `path`: Desired file or directory path (str or PathLike)
- `formatter`: Optional custom formatter function
  - For files: `(base: str, ext: str, n: int) -> str`
  - For directories: `(base: str, n: int) -> str`
- `max_tries`: Safety limit to avoid infinite loops (default: 10,000)
- `create`: If True, atomically create the file/directory (race-safe)

### Returns

- Unused path (str) - absolute or relative, matching input format

### Raises

- `RuntimeError`: If no unused path is found within max_tries
- `OSError`: If file/directory creation fails (when create=True)

## Why unused-path?

When working with file operations, you often need to avoid overwriting existing files:

- ❌ Downloading files that might already exist
- ❌ Creating backup directories with the same name
- ❌ Exporting data to files that may already be present
- ❌ Generating temporary files without conflicts

`unused-path` handles this automatically, similar to how browsers handle duplicate downloads.

## Changelog

See [CHANGELOG.md](https://github.com/ysskrishna/unused-path/blob/main/CHANGELOG.md) for a detailed list of changes and version history.

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/ysskrishna/unused-path/blob/main/CONTRIBUTING.md) for details.

## Support

If you find this library helpful:

- ⭐ Star the repository
- 🐛 Report issues
- 🔀 Submit pull requests
- 💝 [Sponsor on GitHub](https://github.com/sponsors/ysskrishna)

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) - see [LICENSE](https://github.com/ysskrishna/unused-path/blob/main/LICENSE) file for details.

---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://github.com/ysskrishna/unused-path/issues">Report Issues</a> •
  <a href="https://pypi.org/project/unused-path/">Package on PyPI</a>
</p>
