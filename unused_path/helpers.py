"""
Helper functions for unused-path package.

These functions are used internally but can be imported if needed.
"""

import os
import re
import errno
from typing import Tuple

# Regex for parsing numbered suffixes like "file (2)"
SUFFIX_RE = re.compile(r"^(?P<base>.*?)(?: \((?P<num>\d+)\))?$")


def parse_suffix(name: str) -> Tuple[str, int]:
    """
    Parse a name to extract the base name and counter number.
    
    Used internally by both unused_filename and unused_directory.
    
    Args:
        name: The name to parse (e.g., "file (2)", "backup")
    
    Returns:
        Tuple of (base_name: str, counter: int)
        
    Examples:
        >>> parse_suffix("file")
        ('file', 0)
        >>> parse_suffix("file (2)")
        ('file', 2)
        >>> parse_suffix("backup (10)")
        ('backup', 10)
    """
    match = SUFFIX_RE.match(name)
    if not match:
        return name, 0
    
    base = match.group("base")
    num_str = match.group("num")
    counter = int(num_str) if num_str else 0
    
    return base, counter


def try_create_file(path: str) -> bool:
    """
    Atomically create a file if it does not exist.
    
    Uses os.O_EXCL flag to ensure atomic creation, making it safe
    for concurrent access from multiple threads or processes.
    
    Args:
        path: File path to create
    
    Returns:
        True if created successfully, False if already exists
    
    Raises:
        OSError: For errors other than EEXIST (e.g., permission denied)
        
    Examples:
        >>> try_create_file("/tmp/test.txt")
        True
        >>> try_create_file("/tmp/test.txt")  # Already exists
        False
    """
    try:
        # O_CREAT: Create if doesn't exist
        # O_EXCL: Fail if exists (atomic check)
        # O_WRONLY: Open for writing
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o666)
        os.close(fd)
        return True
    except OSError as e:
        if e.errno == errno.EEXIST:
            return False
        raise


def try_create_directory(path: str) -> bool:
    """
    Atomically create a directory if it does not exist.
    
    os.mkdir() is atomic by design, making it safe for concurrent
    access from multiple threads or processes.
    
    Args:
        path: Directory path to create
    
    Returns:
        True if created successfully, False if already exists
    
    Raises:
        OSError: For errors other than EEXIST (e.g., permission denied)
        
    Examples:
        >>> try_create_directory("/tmp/test_dir")
        True
        >>> try_create_directory("/tmp/test_dir")  # Already exists
        False
    """
    try:
        os.mkdir(path, 0o777)
        return True
    except OSError as e:
        if e.errno == errno.EEXIST:
            return False
        raise


def make_full_path(directory: str, name: str) -> str:
    """
    Construct a full path from directory and name components.
    
    Handles empty directory strings correctly (returns just the name).
    
    Args:
        directory: Directory path (can be empty string)
        name: File or directory name
    
    Returns:
        Full path
        
    Examples:
        >>> make_full_path("/home/user", "file.txt")
        '/home/user/file.txt'
        >>> make_full_path("", "file.txt")
        'file.txt'
    """
    return os.path.join(directory, name) if directory else name
