# Installation Guide

Complete installation instructions for AI-Powered DevSecOps Pipeline.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Installation](#local-installation)
3. [Docker Installation](#docker-installation)
4. [Cloud Deployment](#cloud-deployment)
5. [Configuration](#configuration)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (12+), Windows 10/11 with WSL2
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disk**: 10 GB free space
- **Python**: 3.11 or higher

### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disk**: 20+ GB SSD
- **GPU**: Optional (CUDA-compatible for ML acceleration)

### Required Software
- Python 3.11+
- Git
- Docker (optional, for container scanning)
- Node.js 18+ (optional, for web dashboard)

---

## Local Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/APSCRDP.git
cd APSCRDP
```

### 2. Create Virtual Environment

```bash
# Using venv
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n devsecops python=3.11
conda activate devsecops
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install ML model dependencies
pip install -r ml_models/requirements.txt

# Install security scanners
pip install bandit semgrep safety
```

### 4. Install Optional Tools

```bash
# Docker (for container scanning)
# See: https://docs.docker.com/get-docker/

# Trivy (container scanner)
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

### 5. Download ML Models

```bash
# Download pre-trained models (optional - will download on first use)
python -c "
from transformers import AutoTokenizer, AutoModel
AutoTokenizer.from_pretrained('microsoft/codebert-base')
AutoModel.from_pretrained('microsoft/codebert-base')
"
```

---

## Docker Installation

### Quick Start with Docker Compose

```bash
# Clone repository
git clone https://github.com/yourusername/APSCRDP.git
cd APSCRDP

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f devsecops-pipeline

# Stop
docker-compose down
```

### Full Stack (with SonarQube, Grafana)

```bash
# Start all services
docker-compose --profile full up -d

# Access services:
# - SonarQube: http://localhost:9000 (admin/admin)
# - Grafana: http://localhost:3000 (admin/admin)
```

### Building Docker Image Manually

```bash
# Build image
docker build -t ai-devsecops-pipeline:latest .

# Run container
docker run -v $(pwd):/app ai-devsecops-pipeline:latest \
  python scripts/orchestrate_devsecops.py \
  --target sample-apps/vulnerable-flask-app
```

---

## Cloud Deployment

### AWS Deployment

```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Deploy
terraform apply

# Access outputs
terraform output
```

### GitHub Actions (Automated CI/CD)

1. **Fork Repository**
2. **Enable GitHub Actions** in repository settings
3. **Add Secrets** (if using SonarQube, etc.):
   ```
   Settings → Secrets and variables → Actions
   Add: SONAR_TOKEN, SONAR_HOST_URL
   ```
4. **Push Code** - Pipeline runs automatically!

---

## Configuration

### 1. Create Configuration File

```bash
cp config.example.yaml config.yaml
```

### 2. Edit Configuration

```yaml
# config.yaml
scanners:
  bandit:
    enabled: true
    timeout: 300
  semgrep:
    enabled: true
    config: "p/security-audit"

ml_correlation:
  enabled: true
  confidence_threshold: 0.75

deployment_policy:
  max_critical_vulnerabilities: 0
  max_high_vulnerabilities: 5
```

### 3. Set Environment Variables

```bash
# Create .env file
cat > .env <<EOF
PIPELINE_ENV=production
LOG_LEVEL=INFO
ML_MODEL=microsoft/codebert-base
CACHE_ENABLED=true
EOF

# Load environment
source .env
```

---

## Verification

### Test Installation

```bash
# Run self-test
python scripts/orchestrate_devsecops.py \
  --target sample-apps/vulnerable-flask-app \
  --output test-results

# Expected output:
# ✅ SAST Analysis complete
# ✅ ML Correlation complete
# ✅ Report generated
```

### Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=ml_models --cov-report=html
```

### Verify ML Models

```bash
# Test semantic analyzer
python ml_models/semantic_code_analyzer.py

# Test correlation engine
python ml_models/alert_correlation_engine.py
```

---

## Troubleshooting

### Common Issues

#### 1. ImportError: transformers not found

```bash
# Solution: Install ML dependencies
pip install transformers torch
```

#### 2. Semgrep not found

```bash
# Solution: Install via pip
pip install semgrep

# Or via Homebrew (macOS)
brew install semgrep
```

#### 3. Out of memory during ML model loading

```bash
# Solution: Use smaller model
export ML_MODEL=distilbert-base-uncased

# Or increase Docker memory limit
docker run --memory="4g" ...
```

#### 4. Permission denied errors

```bash
# Solution: Fix permissions
chmod +x scripts/*.py
```

### Getting Help

- **Documentation**: See `/documentation` folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/APSCRDP/issues)
- **Community**: [GitHub Discussions](https://github.com/yourusername/APSCRDP/discussions)

---

## Next Steps

1. Review [API Reference](API_REFERENCE.md)
2. Understand [ML Models](ML_MODELS.md)
3. Configure [Policies](../policies/deployment-gate-policy.yaml)
4. Set up [Monitoring](MONITORING.md)

---

**Installation complete!** 🎉

Start scanning:
```bash
python scripts/orchestrate_devsecops.py --target /path/to/your/code
```
