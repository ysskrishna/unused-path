import os
import tempfile
import pytest
from unused_path.helpers import (
    parse_suffix,
    try_create_file,
    try_create_directory,
    make_full_path,
    default_file_formatter,
    default_directory_formatter,
    validate_file_formatter,
    validate_directory_formatter,
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


class TestValidateFileFormatter:
    """Tests for validate_file_formatter."""
    
    def test_valid_formatter(self):
        """Test validation passes for valid formatter."""
        formatter = lambda b, e, n: f"{b}_v{n}{e}"
        validate_file_formatter(formatter)  # Should not raise
    
    def test_default_formatter(self):
        """Test validation passes for default formatter."""
        validate_file_formatter(default_file_formatter)  # Should not raise
    
    def test_not_callable(self):
        """Test validation fails for non-callable."""
        with pytest.raises(TypeError, match="must be callable"):
            validate_file_formatter("not a function")
    
    def test_wrong_parameter_count(self):
        """Test validation fails for wrong parameter count."""
        def wrong_params(b, e):
            return f"{b}{e}"
        
        with pytest.raises(TypeError, match="must accept 3"):
            validate_file_formatter(wrong_params)
    
    def test_wrong_parameter_count_too_many(self):
        """Test validation fails for too many parameters."""
        def too_many_params(b, e, n, extra):
            return f"{b}_{n}{e}"
        
        with pytest.raises(TypeError, match="must accept 3"):
            validate_file_formatter(too_many_params)
    
    def test_wrong_return_type(self):
        """Test validation fails for wrong return type."""
        def returns_int(b, e, n):
            return n
        
        with pytest.raises(TypeError, match="must return str"):
            validate_file_formatter(returns_int)
    
    def test_empty_string_return(self):
        """Test validation fails for empty string return."""
        def empty_formatter(b, e, n):
            return ""
        
        with pytest.raises(ValueError, match="must return non-empty string"):
            validate_file_formatter(empty_formatter)
    
    def test_path_separator_in_result(self):
        """Test validation fails for path separator in result."""
        def bad_formatter(b, e, n):
            return f"{b}{os.sep}{n}{e}"
        
        with pytest.raises(ValueError, match="must not include path separator"):
            validate_file_formatter(bad_formatter)
    
    def test_null_byte_in_result(self):
        """Test validation fails for null byte in result."""
        def bad_formatter(b, e, n):
            return f"{b}\0{n}{e}"
        
        with pytest.raises(ValueError, match="must not include null byte"):
            validate_file_formatter(bad_formatter)
    
    def test_raises_type_error(self):
        """Test validation handles TypeError from formatter."""
        def bad_formatter(b, e, n):
            raise TypeError("Custom error")
        
        with pytest.raises(TypeError, match="must accept 3 arguments"):
            validate_file_formatter(bad_formatter)
    
    def test_raises_other_exception(self):
        """Test validation handles other exceptions from formatter."""
        def bad_formatter(b, e, n):
            raise ValueError("Something went wrong")
        
        with pytest.raises(RuntimeError, match="failed with test arguments"):
            validate_file_formatter(bad_formatter)
    
    def test_valid_with_special_chars(self):
        """Test validation passes with special characters in result."""
        formatter = lambda b, e, n: f"{b}@{n}!{e}"
        validate_file_formatter(formatter)  # Should not raise
    
    def test_valid_with_unicode(self):
        """Test validation passes with unicode characters."""
        formatter = lambda b, e, n: f"{b}→{n}{e}"
        validate_file_formatter(formatter)  # Should not raise


class TestValidateDirectoryFormatter:
    """Tests for validate_directory_formatter."""
    
    def test_valid_formatter(self):
        """Test validation passes for valid formatter."""
        formatter = lambda b, n: f"{b}_v{n}"
        validate_directory_formatter(formatter)  # Should not raise
    
    def test_default_formatter(self):
        """Test validation passes for default formatter."""
        validate_directory_formatter(default_directory_formatter)  # Should not raise
    
    def test_not_callable(self):
        """Test validation fails for non-callable."""
        with pytest.raises(TypeError, match="must be callable"):
            validate_directory_formatter("not a function")
    
    def test_wrong_parameter_count(self):
        """Test validation fails for wrong parameter count."""
        def wrong_params(b):
            return f"{b}"
        
        with pytest.raises(TypeError, match="must accept 2"):
            validate_directory_formatter(wrong_params)
    
    def test_wrong_parameter_count_too_many(self):
        """Test validation fails for too many parameters."""
        def too_many_params(b, n, extra):
            return f"{b}_{n}"
        
        with pytest.raises(TypeError, match="must accept 2"):
            validate_directory_formatter(too_many_params)
    
    def test_wrong_return_type(self):
        """Test validation fails for wrong return type."""
        def returns_int(b, n):
            return n
        
        with pytest.raises(TypeError, match="must return str"):
            validate_directory_formatter(returns_int)
    
    def test_empty_string_return(self):
        """Test validation fails for empty string return."""
        def empty_formatter(b, n):
            return ""
        
        with pytest.raises(ValueError, match="must return non-empty string"):
            validate_directory_formatter(empty_formatter)
    
    def test_path_separator_in_result(self):
        """Test validation fails for path separator in result."""
        def bad_formatter(b, n):
            return f"{b}{os.sep}{n}"
        
        with pytest.raises(ValueError, match="must not include path separator"):
            validate_directory_formatter(bad_formatter)
    
    def test_null_byte_in_result(self):
        """Test validation fails for null byte in result."""
        def bad_formatter(b, n):
            return f"{b}\0{n}"
        
        with pytest.raises(ValueError, match="must not include null byte"):
            validate_directory_formatter(bad_formatter)
    
    def test_raises_type_error(self):
        """Test validation handles TypeError from formatter."""
        def bad_formatter(b, n):
            raise TypeError("Custom error")
        
        with pytest.raises(TypeError, match="must accept 2 arguments"):
            validate_directory_formatter(bad_formatter)
    
    def test_raises_other_exception(self):
        """Test validation handles other exceptions from formatter."""
        def bad_formatter(b, n):
            raise ValueError("Something went wrong")
        
        with pytest.raises(RuntimeError, match="failed with test arguments"):
            validate_directory_formatter(bad_formatter)
    
    def test_valid_with_special_chars(self):
        """Test validation passes with special characters in result."""
        formatter = lambda b, n: f"{b}@{n}!"
        validate_directory_formatter(formatter)  # Should not raise
    
    def test_valid_with_unicode(self):
        """Test validation passes with unicode characters."""
        formatter = lambda b, n: f"{b}→{n}"
        validate_directory_formatter(formatter)  # Should not raise
