"""
Generate unused file and directory paths by auto-incrementing numeric suffixes.

This package helps avoid filename conflicts by automatically appending
numeric suffixes, similar to how browsers handle duplicate downloads.

Examples:
    Basic usage:
        >>> from unused_path import unused_filename, unused_directory
        >>> unused_filename("document.pdf")
        'document.pdf'
        >>> unused_directory("backup")
        'backup'
    
    With atomic creation (race-safe):
        >>> unused_filename("download.zip", create=True)
        'download (1).zip'
        >>> unused_directory("exports", create=True)
        'exports (1)'
    
    Custom formatting:
        >>> unused_filename("log.txt", formatter=lambda b, e, n: f"{b}_{n:03d}{e}")
        'log_001.txt'
        >>> unused_directory("backup", formatter=lambda b, n: f"{b}_v{n}")
        'backup_v1'
"""

from .core import unused_filename, unused_directory

__version__ = "0.1.0"
__all__ = ["unused_filename", "unused_directory"]
