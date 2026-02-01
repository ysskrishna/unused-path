import os
import tempfile
import pytest
from pathlib import Path
from unused_path import unused_filename


class TestUnusedFilenameBasic:
    """Basic functionality tests."""
    
    def test_file_does_not_exist(self):
        """Test when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            result = unused_filename(path)
            assert result == path
    
    def test_file_exists(self):
        """Test when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            open(path, 'w').close()
            
            result = unused_filename(path)
            expected = os.path.join(tmpdir, "test (1).txt")
            assert result == expected
    
    def test_multiple_existing_files(self):
        """Test with multiple existing files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = os.path.join(tmpdir, "test.txt")
            open(base_path, 'w').close()
            open(os.path.join(tmpdir, "test (1).txt"), 'w').close()
            
            result = unused_filename(base_path)
            expected = os.path.join(tmpdir, "test (2).txt")
            assert result == expected
    
    def test_existing_numbered_file(self):
        """Test when input is already numbered."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = os.path.join(tmpdir, "test (2).txt")
            open(os.path.join(tmpdir, "test.txt"), 'w').close()
            open(os.path.join(tmpdir, "test (1).txt"), 'w').close()
            open(os.path.join(tmpdir, "test (2).txt"), 'w').close()
            
            result = unused_filename(base_path)
            expected = os.path.join(tmpdir, "test (3).txt")
            assert result == expected


class TestUnusedFilenameWithCreate:
    """Tests with create=True."""
    
    def test_create_new_file(self):
        """Test creating a new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            result = unused_filename(path, create=True)
            
            assert result == path
            assert os.path.exists(result)
            assert os.path.isfile(result)
    
    def test_create_with_existing_file(self):
        """Test creating when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            open(path, 'w').close()
            
            result = unused_filename(path, create=True)
            expected = os.path.join(tmpdir, "test (1).txt")
            assert result == expected
            assert os.path.exists(result)


class TestUnusedFilenameCustomFormatter:
    """Tests with custom formatters."""
    
    def test_custom_formatter(self):
        """Test with custom formatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            open(path, 'w').close()
            
            formatter = lambda b, e, n: f"{b}_v{n}{e}"
            result = unused_filename(path, formatter=formatter)
            expected = os.path.join(tmpdir, "test_v1.txt")
            assert result == expected
    
    def test_custom_formatter_with_padding(self):
        """Test custom formatter with zero padding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "log.txt")
            open(path, 'w').close()
            
            formatter = lambda b, e, n: f"{b}_{n:03d}{e}"
            result = unused_filename(path, formatter=formatter)
            expected = os.path.join(tmpdir, "log_001.txt")
            assert result == expected


class TestUnusedFilenameEdgeCases:
    """Edge case tests."""
    
    def test_no_extension(self):
        """Test file without extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "Makefile")
            open(path, 'w').close()
            
            result = unused_filename(path)
            expected = os.path.join(tmpdir, "Makefile (1)")
            assert result == expected
    
    def test_empty_directory(self):
        """Test with empty directory (current dir)."""
        path = "test.txt"
        result = unused_filename(path)
        assert result == path
    
    def test_relative_path(self):
        """Test with relative path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                path = "test.txt"
                result = unused_filename(path)
                assert result == path
            finally:
                os.chdir("/")
    
    def test_pathlike_object(self):
        """Test with PathLike object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.txt"
            result = unused_filename(path)
            assert result == str(path)
    
    def test_max_tries(self):
        """Test max_tries limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            # Create many files
            for i in range(100):
                if i == 0:
                    open(path, 'w').close()
                else:
                    open(os.path.join(tmpdir, f"test ({i}).txt"), 'w').close()
            
            with pytest.raises(RuntimeError, match="Unable to find an unused filename"):
                unused_filename(path, max_tries=50)
