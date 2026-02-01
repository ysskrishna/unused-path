import os
import re
import errno
import inspect
from typing import Tuple, Callable

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


def default_file_formatter(base: str, ext: str, n: int) -> str:
    """
    Default formatter for files.
    
    Formats as: "{base} ({n}){ext}" (e.g., "file (1).txt").
    
    Args:
        base: Base filename without extension
        ext: File extension (including the dot)
        n: Counter number
    
    Returns:
        Formatted filename
        
    Examples:
        >>> default_file_formatter("file", ".txt", 1)
        'file (1).txt'
        >>> default_file_formatter("report", ".pdf", 5)
        'report (5).pdf'
        >>> default_file_formatter("Makefile", "", 2)
        'Makefile (2)'
    """
    return f"{base} ({n}){ext}"


def default_directory_formatter(base: str, n: int) -> str:
    """
    Default formatter for directories.
    
    Formats as: "{base} ({n})" (e.g., "backup (1)").
    
    Args:
        base: Base directory name
        n: Counter number
    
    Returns:
        Formatted directory name
        
    Examples:
        >>> default_directory_formatter("backup", 1)
        'backup (1)'
        >>> default_directory_formatter("exports", 3)
        'exports (3)'
    """
    return f"{base} ({n})"


def validate_file_formatter(formatter: Callable[[str, str, int], str]) -> None:
    """
    Validate a file formatter function.
    
    Checks:
    - Is callable
    - Accepts 3 parameters
    - Returns a non-empty string
    - Doesn't include path separators or null bytes
    
    Args:
        formatter: Function to validate
        
    Raises:
        TypeError: If not callable, wrong signature, or wrong return type
        ValueError: If return value is invalid
    """
    # Check if callable
    if not callable(formatter):
        raise TypeError(
            f"File formatter must be callable, got {type(formatter).__name__}"
        )
    
    # Check parameter count (best effort)
    try:
        sig = inspect.signature(formatter)
        param_count = len(sig.parameters)
        if param_count != 3:
            raise TypeError(
                f"File formatter must accept 3 parameters (base, ext, n), "
                f"got {param_count}"
            )
    except (ValueError, TypeError, AttributeError):
        # Can't inspect (built-in, C extension, or special callable)
        # Will validate by calling it instead
        pass
    
    # Test with sample values
    try:
        result = formatter("test", ".txt", 1)
    except TypeError as e:
        raise TypeError(
            f"File formatter must accept 3 arguments (base: str, ext: str, n: int). "
            f"Error: {e}"
        ) from e
    except Exception as e:
        # Use RuntimeError to safely wrap any exception type
        raise RuntimeError(
            f"File formatter failed with test arguments ('test', '.txt', 1): {e}"
        ) from e
    
    # Validate return value
    if not isinstance(result, str):
        raise TypeError(
            f"File formatter must return str, got {type(result).__name__}"
        )
    
    if not result:
        raise ValueError("File formatter must return non-empty string")
    
    # Check for path separators
    if os.sep in result:
        raise ValueError(
            f"File formatter must not include path separator '{os.sep}' in result"
        )
    if os.altsep and os.altsep in result:
        raise ValueError(
            f"File formatter must not include alternate path separator '{os.altsep}' in result"
        )
    
    # Check for null bytes (invalid on all platforms)
    if '\0' in result:
        raise ValueError(
            "File formatter must not include null byte (\\0) in result"
        )


def validate_directory_formatter(formatter: Callable[[str, int], str]) -> None:
    """
    Validate a directory formatter function.
    
    Checks:
    - Is callable
    - Accepts 2 parameters
    - Returns a non-empty string
    - Doesn't include path separators or null bytes
    
    Args:
        formatter: Function to validate
        
    Raises:
        TypeError: If not callable, wrong signature, or wrong return type
        ValueError: If return value is invalid
    """
    # Check if callable
    if not callable(formatter):
        raise TypeError(
            f"Directory formatter must be callable, got {type(formatter).__name__}"
        )
    
    # Check parameter count (best effort)
    try:
        sig = inspect.signature(formatter)
        param_count = len(sig.parameters)
        if param_count != 2:
            raise TypeError(
                f"Directory formatter must accept 2 parameters (base, n), "
                f"got {param_count}"
            )
    except (ValueError, TypeError, AttributeError):
        # Can't inspect - will validate by calling instead
        pass
    
    # Test with sample values
    try:
        result = formatter("test", 1)
    except TypeError as e:
        raise TypeError(
            f"Directory formatter must accept 2 arguments (base: str, n: int). "
            f"Error: {e}"
        ) from e
    except Exception as e:
        # Use RuntimeError to safely wrap any exception type
        raise RuntimeError(
            f"Directory formatter failed with test arguments ('test', 1): {e}"
        ) from e
    
    # Validate return value
    if not isinstance(result, str):
        raise TypeError(
            f"Directory formatter must return str, got {type(result).__name__}"
        )
    
    if not result:
        raise ValueError("Directory formatter must return non-empty string")
    
    # Check for path separators
    if os.sep in result:
        raise ValueError(
            f"Directory formatter must not include path separator '{os.sep}' in result"
        )
    if os.altsep and os.altsep in result:
        raise ValueError(
            f"Directory formatter must not include alternate path separator '{os.altsep}' in result"
        )
    
    # Check for null bytes (invalid on all platforms)
    if '\0' in result:
        raise ValueError(
            "Directory formatter must not include null byte (\\0) in result"
        )
