import os
import tempfile
import threading
from unused_path import unused_filename, unused_directory


class TestRaceConditions:
    """Tests for thread-safety."""
    
    def test_concurrent_file_creation(self):
        """Test concurrent file creation from multiple threads."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = os.path.join(tmpdir, "test.txt")
            results = []
            
            def create():
                results.append(unused_filename(base_path, create=True))
            
            threads = [threading.Thread(target=create) for _ in range(10)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            
            # All should be unique
            assert len(set(results)) == 10
            # All should exist
            assert all(os.path.exists(p) for p in results)
            # All should be files
            assert all(os.path.isfile(p) for p in results)
    
    def test_concurrent_directory_creation(self):
        """Test concurrent directory creation from multiple threads."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = os.path.join(tmpdir, "test_folder")
            results = []
            
            def create():
                results.append(unused_directory(base_path, create=True))
            
            threads = [threading.Thread(target=create) for _ in range(10)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            
            # All should be unique
            assert len(set(results)) == 10
            # All should exist
            assert all(os.path.exists(p) for p in results)
            # All should be directories
            assert all(os.path.isdir(p) for p in results)
    
    def test_mixed_file_and_directory(self):
        """Test files and directories with same base name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file
            file_path = os.path.join(tmpdir, "test")
            open(file_path, 'w').close()
            
            # Try to create a directory with same name
            dir_path = os.path.join(tmpdir, "test")
            result = unused_directory(dir_path)
            
            # Should get test (1) since "test" exists
            expected = os.path.join(tmpdir, "test (1)")
            assert result == expected


class TestComplexScenarios:
    """Tests for complex real-world scenarios."""
    
    def test_gaps_in_sequence(self):
        """Test handling gaps in numbered sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test.txt, test (1).txt, test (3).txt (skip 2)
            open(os.path.join(tmpdir, "test.txt"), 'w').close()
            open(os.path.join(tmpdir, "test (1).txt"), 'w').close()
            open(os.path.join(tmpdir, "test (3).txt"), 'w').close()
            
            # Should fill the gap and use test (2).txt
            result = unused_filename(os.path.join(tmpdir, "test.txt"))
            expected = os.path.join(tmpdir, "test (2).txt")
            assert result == expected
    
    def test_nested_paths(self):
        """Test with nested directory structures."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
            nested = os.path.join(tmpdir, "level1", "level2")
            os.makedirs(nested)
            
            # Create file in nested path
            file_path = os.path.join(nested, "file.txt")
            result = unused_filename(file_path, create=True)
            
            assert result == file_path
            assert os.path.exists(result)
    
    def test_special_characters_in_names(self):
        """Test handling special characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # File with special chars
            path = os.path.join(tmpdir, "file-with_special@chars.txt")
            result = unused_filename(path)
            assert result == path
            
            # Create it and try again
            open(path, 'w').close()
            result = unused_filename(path)
            expected = os.path.join(tmpdir, "file-with_special@chars (1).txt")
            assert result == expected
