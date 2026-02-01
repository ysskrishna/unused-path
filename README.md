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
- **Thread-safe** — Optional atomic file/directory creation for concurrent environments
- **Fully typed** — Complete type hints for excellent IDE autocomplete
- **Battle-tested** — Handles edge cases, gaps in sequences, and special characters

## Installation

```bash
pip install unused-path
```

## Why unused-path?

When working with file operations, you often need to avoid overwriting existing files:

- ❌ Downloading files that might already exist
- ❌ Creating backup directories with the same name
- ❌ Exporting data to files that may already be present
- ❌ Generating temporary files without conflicts

`unused-path` handles this automatically, similar to how browsers handle duplicate downloads.

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

### Thread-Safe Creation

Perfect for multi-threaded applications or concurrent workers:

```python
# Atomically creates the file — no race conditions!
path = unused_filename("download.zip", create=True)
with open(path, 'wb') as f:
    f.write(data)

# Same for directories
export_dir = unused_directory("exports", create=True)
```

### Custom Formatting

```python
# Version numbers with zero-padding
formatter = lambda base, ext, n: f"{base}_v{n:03d}{ext}"
path = unused_filename("log.txt", formatter=formatter)
# → 'log_v001.txt', 'log_v002.txt', ...

# Underscore style
formatter = lambda base, ext, n: f"{base}_{n}{ext}"
path = unused_filename("data.csv", formatter=formatter)
# → 'data_1.csv', 'data_2.csv', ...

# Similar formatting for directories
formatter = lambda base, n: f"{base}_v{n}"
dir_path = unused_directory("backup", formatter=formatter)
# → 'backup_1', 'backup_2', ...
```

## API Reference

| Function | Description |
|----------|-------------|
| `unused_filename(path, *, formatter=None, max_tries=10000, create=False)` | Generate unused filename by appending numeric suffix if needed |
| `unused_directory(path, *, formatter=None, max_tries=10000, create=False)` | Generate unused directory name by appending numeric suffix if needed |

### Parameters

- `path`: Desired directory path (relative or absolute)
- `formatter`: Optional custom formatter function
    | Type | Signature |
    |---------|-----------|
    | File | `(base: str, ext: str, n: int) -> str` |
    | Directory | `(base: str, n: int) -> str` |
- `max_tries`: Maximum attempts to find unused name (default: 10,000)
- `create`: If True, atomically creates the directory to prevent race conditions.
            Useful in multi-threaded/multi-process environments where multiple
            workers might generate directories simultaneously. The created directory
            will be empty and owned by the calling process.

### Returns

- Unused path (str) - preserves the absolute or relative format of the input

### Raises

- `RuntimeError`: If no unused path is found within max_tries attempts
- `OSError`: If file/directory creation fails when create=True (e.g., permission denied)

## Real-World Examples

### Download Manager

```python
import requests
from unused_path import unused_filename

def download_file(url):
    filename = url.split('/')[-1]
    path = unused_filename(filename, create=True)
    
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)
    
    return path
```

### Backup System

```python
from datetime import datetime
from unused_path import unused_directory

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d")
    backup_dir = unused_directory(f"backup_{timestamp}", create=True)
    # ... perform backup ...
    return backup_dir
```

### Data Export

```python
from unused_path import unused_filename

def export_to_csv(data, base_name="export"):
    path = unused_filename(f"{base_name}.csv", create=True)
    data.to_csv(path, index=False)
    print(f"✓ Exported to {path}")
    return path
```

### Temporary Files

```python
from unused_path import unused_filename
import tempfile
import os

def create_temp_file(prefix="temp"):
    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, f"{prefix}.txt")
    return unused_filename(path, create=True)
```


## Advanced Patterns

### Custom Formatter with Timestamp

```python
from datetime import datetime

def timestamp_formatter(base, ext, n):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}_{n}{ext}"

path = unused_filename("log.txt", formatter=timestamp_formatter)
# → 'log_20240115_143052_1.txt'
```

### Limiting Maximum Tries

```python
try:
    path = unused_filename("file.txt", max_tries=100)
except RuntimeError:
    print("Too many files with the same name!")
```

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
