#!/usr/bin/env python3
"""
Project validation script
Checks project structure, files, and basic syntax without requiring dependencies
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple


def check_python_syntax(file_path: Path) -> Tuple[bool, str]:
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def check_required_files() -> List[Tuple[str, bool]]:
    """Check if all required files exist"""
    required_files = [
        "README.md",
        "LICENSE",
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "Makefile",
        "Dockerfile",
        "docker-compose.yml",
        ".gitignore",
        ".dockerignore",
        "CHANGELOG.md",
        "SECURITY.md",
        "pytest.ini",
        "MANIFEST.in",
        ".pre-commit-config.yaml",
        "config.example.yaml",
        "ml_models/__init__.py",
        "ml_models/semantic_code_analyzer.py",
        "ml_models/alert_correlation_engine.py",
        "ml_models/requirements.txt",
        "scripts/__init__.py",
        "scripts/orchestrate_devsecops.py",
        "scripts/run_correlation.py",
        "scripts/generate_security_report.py",
        "scripts/generate_summary.py",
        "scripts/policy_enforcement.py",
        "tests/__init__.py",
        "tests/test_ml_models.py",
        ".github/workflows/devsecops-pipeline.yml",
        "policies/deployment-gate-policy.yaml",
        "documentation/INSTALLATION.md",
        "documentation/API_REFERENCE.md",
        "documentation/CONTRIBUTING.md",
        "sample-apps/vulnerable-flask-app/app.py",
        "sample-apps/vulnerable-flask-app/README.md",
    ]

    results = []
    for file in required_files:
        path = Path(file)
        results.append((file, path.exists()))

    return results


def check_python_files() -> List[Tuple[str, bool, str]]:
    """Check all Python files for syntax errors"""
    python_files = []

    # Find all Python files
    for pattern in ["ml_models/*.py", "scripts/*.py", "tests/*.py", "sample-apps/**/*.py"]:
        python_files.extend(Path(".").glob(pattern))

    results = []
    for py_file in python_files:
        if py_file.name == "__pycache__":
            continue
        valid, msg = check_python_syntax(py_file)
        results.append((str(py_file), valid, msg))

    return results


def main():
    """Run all validation checks"""
    print("=" * 70)
    print("AI-POWERED DEVSECOPS PIPELINE - PROJECT VALIDATION")
    print("=" * 70)
    print()

    # Check required files
    print("📋 Checking Required Files...")
    print("-" * 70)
    file_results = check_required_files()
    missing_files = []

    for file, exists in file_results:
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
        if not exists:
            missing_files.append(file)

    print()
    if missing_files:
        print(f"⚠️  Missing {len(missing_files)} required file(s)")
    else:
        print("✅ All required files present!")

    print()

    # Check Python syntax
    print("🐍 Checking Python Syntax...")
    print("-" * 70)
    python_results = check_python_files()
    syntax_errors = []

    for file, valid, msg in python_results:
        status = "✓" if valid else "✗"
        print(f"  {status} {file}: {msg}")
        if not valid:
            syntax_errors.append((file, msg))

    print()
    if syntax_errors:
        print(f"❌ {len(syntax_errors)} file(s) with syntax errors")
        for file, error in syntax_errors:
            print(f"    - {file}: {error}")
    else:
        print("✅ All Python files have valid syntax!")

    print()

    # Summary
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total files checked: {len(file_results)}")
    print(f"Missing files: {len(missing_files)}")
    print(f"Python files checked: {len(python_results)}")
    print(f"Syntax errors: {len(syntax_errors)}")
    print()

    if not missing_files and not syntax_errors:
        print("🎉 PROJECT VALIDATION PASSED!")
        return 0
    else:
        print("⚠️  PROJECT VALIDATION FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
