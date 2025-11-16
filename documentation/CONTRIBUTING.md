# Contributing to AI-Powered DevSecOps Pipeline

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Pull Request Process](#pull-request-process)
7. [Areas for Contribution](#areas-for-contribution)

---

## Code of Conduct

This project follows a standard code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Assume good intentions
- Prioritize security and quality

---

## How to Contribute

### Reporting Bugs

1. Check existing [GitHub Issues](https://github.com/yourusername/APSCRDP/issues)
2. Create new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages/logs

### Suggesting Features

1. Open a GitHub Discussion or Issue
2. Describe the feature and use case
3. Explain why it would be valuable
4. Consider implementation approach

### Code Contributions

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes
4. Write/update tests
5. Update documentation
6. Submit pull request

---

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/APSCRDP.git
cd APSCRDP
git remote add upstream https://github.com/ORIGINAL-OWNER/APSCRDP.git
```

### 2. Create Development Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 3. Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 4. Run Tests

```bash
pytest tests/ -v --cov=ml_models
```

---

## Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length**: 100 characters max
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Group and sort (isort)
- **Type hints**: Use for function signatures

### Example

```python
from typing import List, Dict, Optional

def analyze_code(
    code: str,
    language: str,
    confidence_threshold: float = 0.75
) -> List[CodeVulnerability]:
    """
    Analyze code for security vulnerabilities.

    Args:
        code: Source code to analyze
        language: Programming language
        confidence_threshold: Minimum confidence for reporting

    Returns:
        List of detected vulnerabilities

    Raises:
        ValueError: If language is not supported
    """
    if not code:
        return []

    # Implementation
    ...
```

### Linting and Formatting

```bash
# Format code
black ml_models/ scripts/

# Check style
flake8 ml_models/ scripts/

# Type checking
mypy ml_models/ scripts/

# Sort imports
isort ml_models/ scripts/
```

---

## Testing

### Unit Tests

All new code must include unit tests:

```python
# tests/test_new_feature.py
import unittest
from ml_models.new_module import NewClass

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.instance = NewClass()

    def test_basic_functionality(self):
        result = self.instance.process("test")
        self.assertEqual(result, expected_value)

    def test_edge_cases(self):
        # Test with empty input
        result = self.instance.process("")
        self.assertIsNone(result)
```

### Integration Tests

Test interactions between components:

```python
def test_full_pipeline():
    """Test complete scan-to-report flow"""
    orchestrator = DevSecOpsOrchestrator()
    result = orchestrator.execute_full_pipeline("test-app/")

    assert result['status'] in ['SUCCESS', 'REJECTED']
    assert 'findings' in result
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_ml_models.py -v

# With coverage
pytest tests/ --cov=ml_models --cov-report=html

# View coverage
open htmlcov/index.html
```

---

## Pull Request Process

### 1. Prepare Changes

```bash
# Sync with upstream
git fetch upstream
git rebase upstream/main

# Run tests
pytest tests/ -v

# Run linters
black .
flake8 .
mypy ml_models/
```

### 2. Commit Messages

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructure
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat(ml): add GPT-based remediation suggestions

Implements GPT-3.5 integration for generating context-aware
remediation guidance for detected vulnerabilities.

Closes #123
```

```
fix(correlation): handle empty alert list correctly

Previously crashed when no alerts were found. Now returns
empty result structure.
```

### 3. Create Pull Request

1. Push to your fork
2. Open PR on GitHub
3. Fill out PR template:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if UI changes)

### 4. Review Process

- Maintainers will review within 48 hours
- Address feedback
- CI must pass (tests, linters)
- Requires 1 approval to merge

---

## Areas for Contribution

### High Priority

1. **Additional ML Models**
   - GPT integration for remediation
   - BERT fine-tuning on security datasets
   - Anomaly detection improvements

2. **Scanner Integrations**
   - GitLeaks (secrets detection)
   - Grype (container scanning)
   - CodeQL (advanced SAST)

3. **Reporting Enhancements**
   - Interactive web dashboard
   - Trend analysis
   - Executive summaries

### Medium Priority

4. **Policy Features**
   - Risk scoring algorithms
   - Exemption workflows
   - Compliance mappings (PCI DSS, SOX)

5. **Performance Optimization**
   - Parallel scanning
   - Incremental analysis
   - Result caching

6. **Documentation**
   - Video tutorials
   - Use case examples
   - API client libraries

### Nice to Have

7. **Integrations**
   - Jira ticket creation
   - Slack notifications
   - Email alerts

8. **Advanced Features**
   - Web UI for results
   - Real-time monitoring
   - Vulnerability tracking

---

## Development Guidelines

### Adding New Scanner

1. Create integration in `security-scanning/`:

```python
# security-scanning/new_scanner.py
class NewScanner:
    def scan(self, target_path: str) -> List[Dict]:
        """Run scanner and return standardized results"""
        # Implementation
        ...
```

2. Add to orchestrator:

```python
# scripts/orchestrate_devsecops.py
def execute_sast(self, target_path: str):
    # ...
    if self.config['scanners']['new_scanner']['enabled']:
        self.run_new_scanner(target_path)
```

3. Update configuration schema
4. Add tests
5. Update documentation

### Adding ML Model

1. Create model in `ml_models/`:

```python
# ml_models/new_model.py
class NewMLModel:
    def __init__(self, model_name: str):
        self.model = load_model(model_name)

    def predict(self, input_data):
        # Implementation
        ...
```

2. Add integration point
3. Include model requirements
4. Add benchmarks
5. Document usage

---

## Questions?

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bugs and features
- **Email**: maintainer@example.com

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
