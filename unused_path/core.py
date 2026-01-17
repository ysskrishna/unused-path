"""
Core implementation for unused-path package.

This module contains the main functions:
- unused_filename: Generate unused file paths
- unused_directory: Generate unused directory paths
"""

import os
import re
import errno
from typing import Callable, Optional
from os import PathLike

# Regex for parsing numbered suffixes like "file (2)"
SUFFIX_RE = re.compile(r"^(?P<base>.*?)(?: \((?P<num>\d+)\))?$")


def unused_filename(
    path: str | PathLike[str],
    *,
    formatter: Optional[Callable[[str, str, int], str]] = None,
    max_tries: int = 10_000,
    create: bool = False,
) -> str:
    """
    Generate an unused filename by appending a numeric suffix if needed.
    
    Handles existing numbered files intelligently:
    - file.txt → file.txt (if available)
    - file.txt → file (1).txt (if file.txt exists)
    - file (2).txt → file (3).txt (continues sequence)
    
    Args:
        path: Desired file path
        formatter: Optional custom formatter function: (base, ext, n) -> filename.
                   If None, uses default formatting "{base} ({n}){ext}".
        max_tries: Safety limit to avoid infinite loops (default: 10,000)
        create: If True, atomically create the file (race-safe)
    
    Returns:
        Unused filename path (absolute or relative, matching input)
    
    Raises:
        RuntimeError: If no unused filename is found within max_tries
        OSError: If file creation fails (when create=True)
    
    Examples:
        >>> unused_filename("document.pdf")
        'document.pdf'
        
        >>> unused_filename("document.pdf", create=True)
        'document (1).pdf'  # if document.pdf exists
        
        >>> unused_filename("report.xlsx", formatter=lambda b, e, n: f"{b}_v{n}{e}")
        'report_v1.xlsx'
    """
    path = os.fspath(path)
    directory, name = os.path.split(path)
    stem, ext = os.path.splitext(name)
    
    # Parse existing numbering
    match = SUFFIX_RE.match(stem)
    if not match:
        base = stem
        counter = 0
    else:
        base = match.group("base")
        num_str = match.group("num")
        counter = int(num_str) if num_str else 0
    
    # Default formatter
    if formatter is None:
        def formatter(base: str, ext: str, n: int) -> str:
            return f"{base} ({n}){ext}"
    
    # Helper to make full path
    def make_full_path(directory: str, name: str) -> str:
        return os.path.join(directory, name) if directory else name
    
    # Helper to try creating file atomically
    def try_create_file(path: str) -> bool:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o666)
            os.close(fd)
            return True
        except OSError as e:
            if e.errno == errno.EEXIST:
                return False
            raise
    
    # Try original path if counter == 0
    if counter == 0:
        candidate = make_full_path(directory, stem + ext)
        if not os.path.exists(candidate):
            if create:
                if try_create_file(candidate):
                    return candidate
            else:
                return candidate
    
    # Try numbered versions
    for _ in range(max_tries):
        counter += 1
        filename = formatter(base, ext, counter)
        candidate = make_full_path(directory, filename)
        
        if not os.path.exists(candidate):
            if create:
                if try_create_file(candidate):
                    return candidate
            else:
                return candidate
    
    raise RuntimeError(
        f"Unable to find an unused filename after {max_tries} attempts"
    )


def unused_directory(
    path: str | PathLike[str],
    *,
    formatter: Optional[Callable[[str, int], str]] = None,
    max_tries: int = 10_000,
    create: bool = False,
) -> str:
    """
    Generate an unused directory name by appending a numeric suffix if needed.
    
    Handles existing numbered directories intelligently:
    - backup → backup (if available)
    - backup → backup (1) (if backup exists)
    - backup (2) → backup (3) (continues sequence)
    
    Args:
        path: Desired directory path
        formatter: Optional custom formatter function: (base, n) -> dirname.
                   If None, uses default formatting "{base} ({n})".
        max_tries: Safety limit to avoid infinite loops (default: 10,000)
        create: If True, atomically create the directory (race-safe)
    
    Returns:
        Unused directory path (absolute or relative, matching input)
    
    Raises:
        RuntimeError: If no unused directory is found within max_tries
        OSError: If directory creation fails (when create=True)
    
    Examples:
        >>> unused_directory("backup")
        'backup'
        
        >>> unused_directory("backup", create=True)
        'backup (1)'  # if backup exists
        
        >>> unused_directory("export_2024", formatter=lambda b, n: f"{b}_{n}")
        'export_2024_1'
    """
    path = os.fspath(path)
    directory, name = os.path.split(path)
    
    # Parse existing numbering
    match = SUFFIX_RE.match(name)
    if not match:
        base = name
        counter = 0
    else:
        base = match.group("base")
        num_str = match.group("num")
        counter = int(num_str) if num_str else 0
    
    # Default formatter
    if formatter is None:
        def formatter(base: str, n: int) -> str:
            return f"{base} ({n})"
    
    # Helper to make full path
    def make_full_path(directory: str, name: str) -> str:
        return os.path.join(directory, name) if directory else name
    
    # Helper to try creating directory atomically
    def try_create_directory(path: str) -> bool:
        try:
            os.mkdir(path, 0o777)
            return True
        except OSError as e:
            if e.errno == errno.EEXIST:
                return False
            raise
    
    # Try original path if counter == 0
    if counter == 0:
        candidate = make_full_path(directory, name)
        if not os.path.exists(candidate):
            if create:
                if try_create_directory(candidate):
                    return candidate
            else:
                return candidate
    
    # Try numbered versions
    for _ in range(max_tries):
        counter += 1
        dirname = formatter(base, counter)
        candidate = make_full_path(directory, dirname)
        
        if not os.path.exists(candidate):
            if create:
                if try_create_directory(candidate):
                    return candidate
            else:
                return candidate
    
    raise RuntimeError(
        f"Unable to find an unused directory name after {max_tries} attempts"
    )
