import os
from typing import Callable, Optional, Union
from os import PathLike

from unused_path.helpers import (
    parse_suffix,
    try_create_file,
    try_create_directory,
    make_full_path,
    validate_file_formatter,
    validate_directory_formatter,
    default_file_formatter,
    default_directory_formatter,
)


def unused_filename(
    path: Union[str, PathLike],
    *,
    formatter: Optional[Callable[[str, str, int], str]] = None,
    max_tries: int = 10_000,
    create: bool = False,
) -> str:
    """
    Generate an unused filename by appending a numeric suffix if needed.
    
    Handles existing numbered files intelligently:
    - "file.txt" → "file.txt" (if available)
    - "file.txt" → "file (1).txt" (if "file.txt" exists)
    - "file (2).txt" → "file (3).txt" (detects "(2)" and continues to "(3)")
    
    Args:
        path: Desired file path (relative or absolute)
        formatter: Optional custom formatter function: (base, ext, n) -> filename.
                   If None, uses default format: "{base} ({n}){ext}"
                   Example: lambda b, e, n: f"{b}_v{n}{e}" → "file_v1.txt"
        max_tries: Maximum attempts to find unused name (default: 10,000)
        create: If True, atomically creates the file to prevent race conditions.
            Useful in multi-threaded/multi-process environments where multiple
            workers might generate files simultaneously. The created file will
            be empty and owned by the calling process.
    
    Returns:
        Path to unused filename (preserves absolute/relative format of input)
    
    Raises:
        RuntimeError: If no unused filename found within max_tries attempts
        OSError: If file creation fails when create=True (e.g., permission denied)
    
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
    base, counter = parse_suffix(stem)
    
    # Use default formatter if none provided
    if formatter is None:
        formatter = default_file_formatter
    else:
        # Validate custom formatter
        validate_file_formatter(formatter)
    
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
    path: Union[str, PathLike],
    *,
    formatter: Optional[Callable[[str, int], str]] = None,
    max_tries: int = 10_000,
    create: bool = False,
) -> str:
    """
    Generate an unused directory name by appending a numeric suffix if needed.
    
    Handles existing numbered directories intelligently:
    - "backup" → "backup" (if available)
    - "backup" → "backup (1)" (if "backup" exists)
    - "backup (2)" → "backup (3)" (detects "(2)" and continues to "(3)")
    
    Args:
        path: Desired directory path (relative or absolute)
        formatter: Optional custom formatter function: (base, n) -> dirname.
                   If None, uses default format: "{base} ({n})"
                   Example: lambda b, n: f"{b}_{n}" → "backup_1"
        max_tries: Maximum attempts to find unused name (default: 10,000)
        create: If True, atomically creates the directory to prevent race conditions.
            Useful in multi-threaded/multi-process environments where multiple
            workers might generate directories simultaneously. The created directory
            will be empty and owned by the calling process.
    
    Returns:
        Path to unused directory (preserves absolute/relative format of input)
    
    Raises:
        RuntimeError: If no unused directory name found within max_tries attempts
        OSError: If directory creation fails when create=True (e.g., permission denied)
    
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
    base, counter = parse_suffix(name)
    
    # Use default formatter if none provided
    if formatter is None:
        formatter = default_directory_formatter
    else:
        # Validate custom formatter
        validate_directory_formatter(formatter)
    
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
