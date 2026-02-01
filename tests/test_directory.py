import os
import tempfile
import pytest
from pathlib import Path
from unused_path import unused_directory


class TestUnusedDirectoryBasic:
    """Basic functionality tests."""
    
    def test_directory_does_not_exist(self):
        """Test when directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_folder")
            result = unused_directory(path)
            assert result == path
    
    def test_directory_exists(self):
        """Test when directory exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_folder")
            os.mkdir(path)
            
            result = unused_directory(path)
            expected = os.path.join(tmpdir, "test_folder (1)")
            assert result == expected
    
    def test_multiple_existing_directories(self):
        """Test with multiple existing directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = os.path.join(tmpdir, "test_folder")
            os.mkdir(base_path)
            os.mkdir(os.path.join(tmpdir, "test_folder (1)"))
            
            result = unused_directory(base_path)
            expected = os.path.join(tmpdir, "test_folder (2)")
            assert result == expected
    
    def test_existing_numbered_directory(self):
        """Test when input is already numbered."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = os.path.join(tmpdir, "test_folder (2)")
            os.mkdir(os.path.join(tmpdir, "test_folder"))
            os.mkdir(os.path.join(tmpdir, "test_folder (1)"))
            os.mkdir(os.path.join(tmpdir, "test_folder (2)"))
            
            result = unused_directory(base_path)
            expected = os.path.join(tmpdir, "test_folder (3)")
            assert result == expected


class TestUnusedDirectoryWithCreate:
    """Tests with create=True."""
    
    def test_create_new_directory(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_folder")
            result = unused_directory(path, create=True)
            
            assert result == path
            assert os.path.exists(result)
            assert os.path.isdir(result)
    
    def test_create_with_existing_directory(self):
        """Test creating when directory exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_folder")
            os.mkdir(path)
            
            result = unused_directory(path, create=True)
            expected = os.path.join(tmpdir, "test_folder (1)")
            assert result == expected
            assert os.path.exists(result)


class TestUnusedDirectoryCustomFormatter:
    """Tests with custom formatters."""
    
    def test_custom_formatter(self):
        """Test with custom formatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "backup")
            os.mkdir(path)
            
            formatter = lambda b, n: f"{b}_v{n}"
            result = unused_directory(path, formatter=formatter)
            expected = os.path.join(tmpdir, "backup_v1")
            assert result == expected
    
    def test_custom_formatter_with_padding(self):
        """Test custom formatter with zero padding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "export")
            os.mkdir(path)
            
            formatter = lambda b, n: f"{b}_{n:03d}"
            result = unused_directory(path, formatter=formatter)
            expected = os.path.join(tmpdir, "export_001")
            assert result == expected


class TestUnusedDirectoryEdgeCases:
    """Edge case tests."""
    
    def test_empty_directory(self):
        """Test with empty directory (current dir)."""
        path = "test_folder"
        result = unused_directory(path)
        assert result == path
    
    def test_relative_path(self):
        """Test with relative path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                path = "test_folder"
                result = unused_directory(path)
                assert result == path
            finally:
                os.chdir("/")
    
    def test_pathlike_object(self):
        """Test with PathLike object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test_folder"
            result = unused_directory(path)
            assert result == str(path)
    
    def test_max_tries(self):
        """Test max_tries limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_folder")
            # Create many directories
            for i in range(100):
                if i == 0:
                    os.mkdir(path)
                else:
                    os.mkdir(os.path.join(tmpdir, f"test_folder ({i})"))
            
            with pytest.raises(RuntimeError, match="Unable to find an unused directory"):
                unused_directory(path, max_tries=50)
