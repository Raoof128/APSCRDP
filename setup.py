#!/usr/bin/env python3
"""
Setup configuration for AI-Powered DevSecOps Pipeline
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    req_file = Path(__file__).parent / filename
    if not req_file.exists():
        return []

    requirements = []
    with open(req_file) as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Remove version constraints for basic listing
                requirements.append(line)
    return requirements

setup(
    name="ai-devsecops-pipeline",
    version="1.0.0",
    author="APSCRDP Team",
    author_email="security@example.com",
    description="AI-Powered Secure Code Review & DevSecOps Pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/APSCRDP",
    packages=find_packages(exclude=["tests", "tests.*", "sample-apps", "sample-apps.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "scikit-learn>=1.3.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "jinja2>=3.1.2",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "joblib>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.0.0",
        ],
        "scanners": [
            "bandit>=1.7.5",
            "semgrep>=1.40.0",
            "safety>=2.3.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "devsecops-scan=scripts.orchestrate_devsecops:main",
            "devsecops-correlate=scripts.run_correlation:main",
            "devsecops-report=scripts.generate_security_report:main",
            "devsecops-policy=scripts.policy_enforcement:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json"],
    },
    zip_safe=False,
)
