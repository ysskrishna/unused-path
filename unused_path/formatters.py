"""
Formatter functions for unused-path package.

These functions provide default formatting behavior for numbered paths.
They can be imported if needed for custom formatting.
"""


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
