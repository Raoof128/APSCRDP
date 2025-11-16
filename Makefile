# Makefile for AI-Powered DevSecOps Pipeline
# Common development and operations tasks

.PHONY: help install install-dev test lint format clean docker-build docker-run scan

# Default target
help:
	@echo "AI-Powered DevSecOps Pipeline - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install package and dependencies"
	@echo "  make install-dev      Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test            Run test suite"
	@echo "  make test-cov        Run tests with coverage report"
	@echo "  make lint            Run code linters"
	@echo "  make format          Auto-format code with black"
	@echo "  make type-check      Run mypy type checking"
	@echo ""
	@echo "Scanning:"
	@echo "  make scan            Run security scan on sample app"
	@echo "  make scan-self       Run security scan on this project"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    Build Docker image"
	@echo "  make docker-run      Run pipeline in Docker"
	@echo "  make docker-compose  Start full stack with docker-compose"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean           Remove generated files"
	@echo "  make clean-all       Deep clean including caches"
	@echo ""

# Installation targets
install:
	pip install -e .
	pip install bandit semgrep safety

install-dev:
	pip install -e ".[dev,scanners]"
	pip install -r requirements-dev.txt
	pre-commit install

# Testing targets
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=ml_models --cov=scripts --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

test-ml:
	pytest tests/test_ml_models.py -v -m ml

test-integration:
	pytest tests/ -v -m integration

# Code quality targets
lint:
	@echo "Running flake8..."
	flake8 ml_models/ scripts/ tests/
	@echo "Running pylint..."
	pylint ml_models/ scripts/ || true
	@echo "Running bandit on codebase..."
	bandit -r ml_models/ scripts/ -ll || true

format:
	@echo "Formatting with black..."
	black ml_models/ scripts/ tests/
	@echo "Sorting imports with isort..."
	isort ml_models/ scripts/ tests/

type-check:
	mypy ml_models/ scripts/

# Scanning targets
scan:
	python scripts/orchestrate_devsecops.py \
		--target sample-apps/vulnerable-flask-app \
		--output scan-results/sample-app

scan-self:
	python scripts/orchestrate_devsecops.py \
		--target . \
		--output scan-results/self-scan

# Docker targets
docker-build:
	docker build -t ai-devsecops-pipeline:latest .

docker-run:
	docker run -v $(PWD):/app ai-devsecops-pipeline:latest

docker-compose:
	docker-compose up -d

docker-compose-full:
	docker-compose --profile full up -d

docker-stop:
	docker-compose down

# Maintenance targets
clean:
	@echo "Cleaning generated files..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + || true
	rm -rf build/ dist/ .eggs/
	rm -rf htmlcov/ .coverage
	rm -rf .pytest_cache/
	rm -rf scan-results/*
	@echo "Clean complete!"

clean-all: clean
	@echo "Deep cleaning..."
	rm -rf .cache/
	rm -rf venv/ env/
	rm -rf *.db *.sqlite
	rm -rf .mypy_cache/
	rm -rf .tox/
	@echo "Deep clean complete!"

# Development workflow
dev-setup: install-dev
	@echo "Creating example config..."
	cp config.example.yaml config.yaml || true
	@echo "Development environment ready!"

# Quick validation
validate:
	@echo "Validating Python syntax..."
	python -m py_compile ml_models/*.py scripts/*.py
	@echo "Validating YAML files..."
	python -c "import yaml; yaml.safe_load(open('.github/workflows/devsecops-pipeline.yml'))"
	python -c "import yaml; yaml.safe_load(open('policies/deployment-gate-policy.yaml'))"
	@echo "Validation complete!"

# Build and publish (for maintainers)
build:
	python -m build

publish-test:
	python -m twine upload --repository testpypi dist/*

publish:
	python -m twine upload dist/*
