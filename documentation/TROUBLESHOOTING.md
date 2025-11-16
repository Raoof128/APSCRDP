# Troubleshooting Guide

## AI-Powered DevSecOps Pipeline - Common Issues & Solutions

This guide covers common issues, error messages, and their solutions.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Scanning Errors](#scanning-errors)
3. [ML Model Problems](#ml-model-problems)
4. [GitHub Actions Failures](#github-actions-failures)
5. [Docker Issues](#docker-issues)
6. [Performance Problems](#performance-problems)
7. [Configuration Errors](#configuration-errors)
8. [Reporting Issues](#reporting-issues)

---

## Installation Issues

### Error: "Command not found: bandit/semgrep/safety"

**Symptom**:
```
bash: bandit: command not found
```

**Cause**: Security scanners not installed

**Solution**:
```bash
# Install all scanners
pip install bandit semgrep safety

# Verify installation
bandit --version
semgrep --version
safety --version
```

---

### Error: "ModuleNotFoundError: No module named 'transformers'"

**Symptom**:
```python
ModuleNotFoundError: No module named 'transformers'
```

**Cause**: ML dependencies not installed

**Solution**:
```bash
# Install ML dependencies
pip install -r ml_models/requirements.txt

# Or install specific packages
pip install torch transformers scikit-learn pandas numpy
```

---

### Error: "Permission denied" when running scripts

**Symptom**:
```
bash: ./scripts/orchestrate_devsecops.py: Permission denied
```

**Cause**: Scripts not executable

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.py
chmod +x ml_models/*.py

# Or run with python
python scripts/orchestrate_devsecops.py
```

---

## Scanning Errors

### Error: "Bandit crashed with exit code 1"

**Symptom**:
```
ERROR: Bandit failed: Process exited with code 1
```

**Cause**: Bandit found critical issues or crashed

**Solution**:
```bash
# Run Bandit manually to see detailed error
bandit -r /path/to/code -ll

# Check if path exists
ls -la /path/to/code

# Try with verbose output
bandit -r /path/to/code -v
```

**Common Causes**:
1. Invalid Python syntax in scanned code
2. Permission issues reading files
3. Bandit configuration error

---

### Error: "Semgrep timeout"

**Symptom**:
```
ERROR: Semgrep timed out after 600 seconds
```

**Cause**: Large codebase or complex rules

**Solution**:
```bash
# Increase timeout in config.yaml
scanners:
  semgrep:
    timeout: 1200  # 20 minutes

# Or scan specific directories
semgrep --config p/security-audit specific_dir/

# Use faster rules
semgrep --config auto
```

---

### Error: "Safety check failed: Network error"

**Symptom**:
```
ERROR: Could not connect to Safety DB
```

**Cause**: Network connectivity or Safety API unavailable

**Solution**:
```bash
# Check internet connection
ping pyup.io

# Use cached database
safety check --offline

# Try with proxy if behind corporate firewall
export HTTP_PROXY=http://proxy:port
safety check
```

---

## ML Model Problems

### Error: "CUDA out of memory"

**Symptom**:
```
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Cause**: GPU memory insufficient for model

**Solution**:
```bash
# Force CPU usage
export CUDA_VISIBLE_DEVICES=""

# Or in Python code
analyzer = SemanticCodeAnalyzer(device="cpu")

# Reduce batch size
analyzer = SemanticCodeAnalyzer(batch_size=1)
```

---

### Error: "Model download failed"

**Symptom**:
```
OSError: Can't load weights for 'microsoft/codebert-base'
```

**Cause**: Network issue or HuggingFace Hub unavailable

**Solution**:
```bash
# Pre-download model
python -c "
from transformers import AutoModel, AutoTokenizer
AutoTokenizer.from_pretrained('microsoft/codebert-base')
AutoModel.from_pretrained('microsoft/codebert-base')
"

# Use offline mode (after download)
export TRANSFORMERS_OFFLINE=1

# Use different model
analyzer = SemanticCodeAnalyzer(model_name="distilbert-base-uncased")
```

---

### Error: "False positive rate too high"

**Symptom**: ML correlation not filtering enough alerts

**Cause**: Model not trained on your data

**Solution**:
```bash
# Train on your feedback data
python scripts/train_correlation.py \
  --feedback labeled_alerts.json \
  --output models/custom_classifier.pkl

# Adjust threshold
ml_correlation:
  fp_threshold: 0.90  # More aggressive filtering
```

---

## GitHub Actions Failures

### Error: "Workflow run failed: permission denied"

**Symptom**:
```
Error: Resource not accessible by integration
```

**Cause**: Insufficient permissions in workflow

**Solution**:

Edit `.github/workflows/devsecops-pipeline.yml`:
```yaml
permissions:
  contents: read
  security-events: write
  pull-requests: write  # Add this
```

---

### Error: "Artifact upload failed"

**Symptom**:
```
Error: Unable to upload artifact
```

**Cause**: Artifact too large or path invalid

**Solution**:
```yaml
# Compress large artifacts
- name: Compress reports
  run: tar -czf reports.tar.gz scan-results/

- name: Upload
  uses: actions/upload-artifact@v4
  with:
    name: reports
    path: reports.tar.gz
```

---

### Error: "SARIF upload failed"

**Symptom**:
```
Error: Invalid SARIF file format
```

**Cause**: Malformed SARIF JSON

**Solution**:
```bash
# Validate SARIF locally
cat results.sarif | jq empty

# Check against schema
npm install -g @microsoft/sarif-multitool
sarif validate results.sarif
```

---

## Docker Issues

### Error: "Docker build failed: no such file or directory"

**Symptom**:
```
Step 5/10 : COPY requirements.txt /app/
COPY failed: no source files were specified
```

**Cause**: File not in build context

**Solution**:
```bash
# Ensure you're in project root
cd /path/to/APSCRDP

# Build from correct directory
docker build -t ai-devsecops-pipeline .

# Check .dockerignore isn't excluding needed files
cat .dockerignore
```

---

### Error: "Container exits immediately"

**Symptom**: Container starts but exits with code 0

**Cause**: No foreground process

**Solution**:
```bash
# Run with interactive mode
docker run -it ai-devsecops-pipeline /bin/bash

# Or specify command
docker run ai-devsecops-pipeline \
  python scripts/orchestrate_devsecops.py --help
```

---

### Error: "Out of disk space"

**Symptom**:
```
Error: no space left on device
```

**Cause**: Docker images/volumes consuming space

**Solution**:
```bash
# Clean up Docker
docker system prune -a

# Remove unused volumes
docker volume prune

# Check space
df -h
```

---

## Performance Problems

### Issue: "Scans take >10 minutes"

**Symptoms**: Pipeline very slow

**Diagnosis**:
```bash
# Run with timing
time python scripts/orchestrate_devsecops.py --target app/

# Check which scanner is slow
python scripts/orchestrate_devsecops.py --target app/ --debug
```

**Solutions**:

1. **Enable parallel execution**:
```yaml
# config.yaml
advanced:
  parallel_execution: true
  max_workers: 4
```

2. **Enable caching**:
```yaml
cache:
  enabled: true
  directory: .cache
  ttl: 86400
```

3. **Scan only changed files** (Git):
```bash
# Get changed files
git diff --name-only HEAD~1

# Scan only those
python scripts/orchestrate_devsecops.py --target $(git diff --name-only HEAD~1)
```

4. **Reduce scanners**:
```yaml
scanners:
  trivy:
    enabled: false  # Disable slow scanners
```

---

### Issue: "High memory usage"

**Symptoms**: System running out of RAM

**Solutions**:

1. **Use CPU instead of GPU**:
```python
analyzer = SemanticCodeAnalyzer(device="cpu")
```

2. **Reduce batch size**:
```python
analyzer = SemanticCodeAnalyzer(batch_size=1)
```

3. **Disable ML models**:
```yaml
ml_correlation:
  enabled: false
```

4. **Run in Docker with memory limits**:
```bash
docker run --memory="2g" ai-devsecops-pipeline
```

---

## Configuration Errors

### Error: "Invalid YAML configuration"

**Symptom**:
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Cause**: YAML syntax error

**Solution**:
```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Check indentation (use spaces, not tabs)
cat -A config.yaml

# Use online validator
# yamllint.com
```

---

### Error: "Configuration key not found"

**Symptom**:
```
KeyError: 'scanners'
```

**Cause**: Missing configuration section

**Solution**:
```bash
# Copy example config
cp config.example.yaml config.yaml

# Edit with required values
nano config.yaml
```

---

### Error: "Policy file not found"

**Symptom**:
```
FileNotFoundError: policies/deployment-gate-policy.yaml
```

**Cause**: Policy file missing or wrong path

**Solution**:
```bash
# Check file exists
ls -la policies/deployment-gate-policy.yaml

# Use absolute path
python scripts/policy_enforcement.py \
  --policy /full/path/to/policy.yaml

# Create from template
cp policies/deployment-gate-policy.yaml.example \
   policies/deployment-gate-policy.yaml
```

---

## Reporting Issues

### Error: "HTML report generation failed"

**Symptom**:
```
ERROR: Failed to generate HTML report
```

**Cause**: Missing template or data

**Solution**:
```bash
# Check findings file exists
ls -la consolidated-findings.json

# Generate with verbose mode
python scripts/generate_security_report.py \
  --findings consolidated-findings.json \
  --format html \
  --output report.html \
  --verbose

# Use JSON format as fallback
python scripts/generate_security_report.py \
  --format json \
  --output report.json
```

---

### Error: "No findings in report"

**Symptom**: Report shows 0 vulnerabilities despite issues existing

**Cause**: Correlation filtering too aggressive or no alerts found

**Solution**:
```bash
# Check raw scanner outputs
ls -la scan-results/

# Lower FP threshold
ml_correlation:
  fp_threshold: 0.50  # Less aggressive

# Check if scanners ran
cat scan-results/bandit-report.json
```

---

## Getting More Help

### Enable Debug Logging

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run with verbose output
python scripts/orchestrate_devsecops.py \
  --target app/ \
  --verbose \
  --debug
```

### Check Logs

```bash
# Pipeline logs
cat devsecops-pipeline.log

# GitHub Actions logs
# Go to Actions tab → Click on workflow run → View logs

# Docker logs
docker logs <container-id>
```

### Generate Diagnostic Report

```bash
# System info
python --version
pip list

# Scanner versions
bandit --version
semgrep --version

# Disk space
df -h

# Memory
free -h
```

---

## Still Having Issues?

1. **Search Existing Issues**: [GitHub Issues](https://github.com/yourusername/APSCRDP/issues)
2. **Ask the Community**: [GitHub Discussions](https://github.com/yourusername/APSCRDP/discussions)
3. **Report Bug**: Use [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
4. **Email Support**: security@example.com

---

## Common Error Messages Quick Reference

| Error | Quick Fix |
|-------|-----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `Command not found` | `pip install bandit semgrep safety` |
| `Permission denied` | `chmod +x scripts/*.py` |
| `CUDA out of memory` | Add `device="cpu"` to analyzer |
| `Network error` | Check internet connection |
| `Invalid YAML` | Validate with `yamllint` |
| `Timeout` | Increase timeout in config |
| `Out of disk space` | `docker system prune -a` |

---

**Last Updated**: 2025-11-16
**Maintained By**: APSCRDP Team
