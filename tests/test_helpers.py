"""Tests for helper functions."""

import os
import tempfile
import pytest
from unused_path.helpers import (
    parse_suffix,
    try_create_file,
    try_create_directory,
    make_full_path,
)
from unused_path.formatters import (
    default_file_formatter,
    default_directory_formatter,
)


class TestParseSuffix:
    """Tests for parse_suffix helper."""
    
    def test_no_suffix(self):
        """Test parsing name without suffix."""
        base, counter = parse_suffix("file")
        assert base == "file"
        assert counter == 0
    
    def test_with_suffix(self):
        """Test parsing name with suffix."""
        base, counter = parse_suffix("file (2)")
        assert base == "file"
        assert counter == 2
    
    def test_large_number(self):
        """Test parsing with large number."""
        base, counter = parse_suffix("backup (999)")
        assert base == "backup"
        assert counter == 999
    
    def test_zero_suffix(self):
        """Test parsing with zero suffix."""
        base, counter = parse_suffix("file (0)")
        assert base == "file"
        assert counter == 0
    
    def test_parentheses_in_name(self):
        """Test name containing parentheses."""
        base, counter = parse_suffix("report (Q1)")
        assert base == "report (Q1)"
        assert counter == 0
    
    def test_multiple_spaces(self):
        """Test name with multiple spaces."""
        base, counter = parse_suffix("my file")
        assert base == "my file"
        assert counter == 0
    
    def test_trailing_spaces(self):
        """Test name with trailing spaces."""
        base, counter = parse_suffix("file ")
        assert base == "file "
        assert counter == 0
    
    def test_complex_name(self):
        """Test complex filename."""
        base, counter = parse_suffix("report (2023) final")
        assert base == "report (2023) final"
        assert counter == 0


class TestTryCreateFile:
    """Tests for try_create_file helper."""
    
    def test_create_new_file(self):
        """Test creating a new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            
            result = try_create_file(path)
            assert result is True
            assert os.path.exists(path)
            assert os.path.isfile(path)
    
    def test_file_already_exists(self):
        """Test when file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            
            # Create first time
            result1 = try_create_file(path)
            assert result1 is True
            
            # Try again
            result2 = try_create_file(path)
            assert result2 is False
    
    def test_permission_error(self):
        """Test permission errors."""
        with pytest.raises(OSError):
            try_create_file("/root/forbidden.txt")
    
    def test_invalid_path(self):
        """Test invalid path."""
        with pytest.raises(OSError):
            try_create_file("/nonexistent/directory/file.txt")


class TestTryCreateDirectory:
    """Tests for try_create_directory helper."""
    
    def test_create_new_directory(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_dir")
            
            result = try_create_directory(path)
            assert result is True
            assert os.path.exists(path)
            assert os.path.isdir(path)
    
    def test_directory_already_exists(self):
        """Test when directory already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_dir")
            
            # Create first time
            result1 = try_create_directory(path)
            assert result1 is True
            
            # Try again
            result2 = try_create_directory(path)
            assert result2 is False
    
    def test_permission_error(self):
        """Test permission errors."""
        with pytest.raises(OSError):
            try_create_directory("/root/forbidden_dir")
    
    def test_invalid_path(self):
        """Test invalid path."""
        with pytest.raises(OSError):
            try_create_directory("/nonexistent/parent/directory")


class TestMakeFullPath:
    """Tests for make_full_path helper."""
    
    def test_with_directory(self):
        """Test with directory."""
        result = make_full_path("/home/user", "file.txt")
        assert result == "/home/user/file.txt"
    
    def test_empty_directory(self):
        """Test with empty directory."""
        result = make_full_path("", "file.txt")
        assert result == "file.txt"
    
    def test_relative_directory(self):
        """Test with relative directory."""
        result = make_full_path("../data", "file.txt")
        assert result == "../data/file.txt"
    
    def test_multiple_components(self):
        """Test with multiple path components."""
        result = make_full_path("/var/data/backup", "file.txt")
        assert result == "/var/data/backup/file.txt"


class TestFileFormatter:
    """Tests for default_file_formatter."""
    
    def test_basic_formatting(self):
        """Test basic file formatting."""
        result = default_file_formatter("file", ".txt", 1)
        assert result == "file (1).txt"
    
    def test_no_extension(self):
        """Test file without extension."""
        result = default_file_formatter("Makefile", "", 5)
        assert result == "Makefile (5)"
    
    def test_large_number(self):
        """Test with large number."""
        result = default_file_formatter("file", ".txt", 999)
        assert result == "file (999).txt"
    
    def test_multiple_dots(self):
        """Test with multiple dots in extension."""
        result = default_file_formatter("archive.tar", ".gz", 2)
        assert result == "archive.tar (2).gz"


class TestDirectoryFormatter:
    """Tests for default_directory_formatter."""
    
    def test_basic_formatting(self):
        """Test basic directory formatting."""
        result = default_directory_formatter("backup", 1)
        assert result == "backup (1)"
    
    def test_large_number(self):
        """Test with large number."""
        result = default_directory_formatter("backup", 999)
        assert result == "backup (999)"
    
    def test_complex_name(self):
        """Test with complex directory name."""
        result = default_directory_formatter("my backup folder", 5)
        assert result == "my backup folder (5)"
