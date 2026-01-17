# Contributing to unused-path

Thank you for your interest in contributing to `unused-path`! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv)

### Setting Up the Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ysskrishna/unused-path.git
   cd unused-path
   ```

2. **Install dependencies**:
   ```bash
   uv sync --group dev
   ```

3. **Verify the setup**:
   ```bash
   uv run pytest
   ```

## Development Workflow

### Running Tests

Run the test suite to ensure everything works:

```bash
uv run pytest
```

Run a specific test file:

```bash
uv run pytest tests/test_filename.py
```

### Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function parameters and return values
- Keep functions simple and focused
- Add docstrings to all public functions

### Improving Functionality

If you want to improve unused-path functionality:

1. Edit `unused_path/core.py` for main functions
2. Edit `unused_path/helpers.py` for helper functions
3. Edit `unused_path/formatters.py` for formatter functions
4. Ensure the functions handle errors gracefully
5. Add corresponding test cases in the test files
6. Run the test suite to ensure everything passes

### Writing Tests

- All new features should include tests
- Tests should be placed in the `tests/` directory
- Test both positive cases and negative cases
- Consider edge cases and error handling:
  - Empty inputs
  - Invalid inputs
  - Race conditions
  - Special characters in names
  - Gaps in numbered sequences
  - Nested directory structures
- Test both `unused_filename()` and `unused_directory()` functions

## Submitting Changes

### Pull Request Process

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-fix-name
   ```

2. **Make your changes**:
   - Write your code
   - Add tests for new functionality
   - Ensure all tests pass
   - Update documentation if needed

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```
   
   Use clear, descriptive commit messages. Follow the format:
   - `feat: add new feature`
   - `fix: fix bug description`
   - `docs: update documentation`
   - `test: add tests for feature`
   - `refactor: improve code structure`

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR description with:
     - Description of changes
     - Related issues (if any)
     - Testing instructions

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Ensure all tests pass
- Update documentation if you're adding new features
- Write clear commit messages
- Reference any related issues

## Reporting Issues

When reporting issues, please include:

- Python version
- Package version
- Operating system and version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Any relevant error messages or stack traces

## Code of Conduct

- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Be open to feedback and suggestions

## Questions?

If you have questions about contributing, feel free to:

- Open an issue on GitHub
- Check existing issues and discussions

Thank you for contributing to `unused-path`! 🎉
