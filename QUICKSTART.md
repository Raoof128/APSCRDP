# Quick Start Guide

Get the AI-Powered DevSecOps Pipeline running in **5 minutes**.

## Option 1: Local Installation (Recommended for Development)

### Prerequisites
- Python 3.11+ installed
- 4GB+ RAM available
- 5GB+ free disk space

### Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/APSCRDP.git
cd APSCRDP

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies (without ML models for quick start)
pip install --upgrade pip
pip install bandit semgrep safety pyyaml

# 4. Run quick scan on sample vulnerable app
python scripts/orchestrate_devsecops.py \
  --target sample-apps/vulnerable-flask-app \
  --output quick-scan-results

# 5. View results
cat quick-scan-results/scan-results/security-assessment-report.json
```

**Expected Output:**
```
🚀 Starting AI-Powered DevSecOps Pipeline
├─ 🔍 Running SAST Analysis...
│  ├─ Bandit: 8 issues (3 critical, 5 high)
│  └─ Semgrep: 5 issues found
├─ 📋 Running Dependency Scanning...
│  └─ Safety: 3 vulnerabilities found
└─ ✅ Report saved to quick-scan-results/
```

---

## Option 2: Docker (Easiest)

### Prerequisites
- Docker installed
- 2GB+ free disk space

### Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/APSCRDP.git
cd APSCRDP

# 2. Build and run
docker-compose up devsecops-pipeline

# 3. Results will be in scan-results/
```

---

## Option 3: GitHub Actions (Zero Installation)

### Steps

1. **Fork** this repository
2. **Enable GitHub Actions** in Settings
3. **Push code** - pipeline runs automatically!

```bash
git clone https://github.com/YOURUSERNAME/APSCRDP.git
cd APSCRDP
echo "# Test change" >> README.md
git add README.md
git commit -m "test: trigger pipeline"
git push origin main
```

4. **View results** in the Actions tab

---

## Quick Test: Scan Your Own Project

Once installed, scan any Python project:

```bash
# Activate virtual environment (if using local install)
source venv/bin/activate

# Scan your project
python scripts/orchestrate_devsecops.py \
  --target /path/to/your/project \
  --output my-scan-results

# View HTML report
open my-scan-results/security-assessment-report.html
```

---

## Understanding the Results

### Result Files

```
scan-results/
├── bandit-report.json          # Python SAST results
├── semgrep-report.json         # Multi-language SAST
├── safety-report.json          # Dependency vulnerabilities
├── consolidated-findings.json  # ML-correlated results
└── security-assessment-report.json  # Final report
```

### Severity Levels

- **CRITICAL**: Immediate action required
- **HIGH**: Fix before deployment
- **MEDIUM**: Fix in next sprint
- **LOW**: Track and address over time

---

## What's Next?

### Enable Full ML Features

```bash
# Install ML dependencies (larger download)
pip install -r ml_models/requirements.txt

# Run with ML-powered analysis
python scripts/orchestrate_devsecops.py \
  --target sample-apps/vulnerable-flask-app \
  --output full-ml-scan
```

### Customize Security Policies

```bash
# Copy example configuration
cp config.example.yaml config.yaml

# Edit thresholds
nano config.yaml  # or vim/code/etc.

# Run with custom config
python scripts/orchestrate_devsecops.py \
  --config config.yaml \
  --target your-project/
```

### Integrate with CI/CD

See [documentation/INSTALLATION.md](documentation/INSTALLATION.md) for:
- GitHub Actions integration
- GitLab CI setup
- Jenkins pipeline
- Pre-commit hooks

---

## Common Issues

### Issue: "Command not found: bandit/semgrep"

**Solution:**
```bash
pip install bandit semgrep safety
```

### Issue: "Out of memory during ML model loading"

**Solution:** Use CPU-only mode or smaller model:
```bash
# Skip ML models for faster scanning
python scripts/orchestrate_devsecops.py \
  --target your-project/ \
  --skip-ml
```

### Issue: "Permission denied"

**Solution:**
```bash
chmod +x scripts/*.py
```

---

## Need Help?

- 📖 **Full Documentation**: [documentation/INSTALLATION.md](documentation/INSTALLATION.md)
- 🐛 **Report Bug**: [GitHub Issues](https://github.com/yourusername/APSCRDP/issues)
- 💬 **Ask Questions**: [GitHub Discussions](https://github.com/yourusername/APSCRDP/discussions)
- 📧 **Email**: security@example.com

---

## Quick Commands Reference

```bash
# Run validation
make validate

# Run tests
make test

# Scan sample app
make scan

# Scan this project
make scan-self

# Format code
make format

# View all commands
make help
```

---

**Congratulations!** 🎉 You're now running an AI-powered security pipeline!

Next: Read the [full README](README.md) for advanced features.
