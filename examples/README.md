# Examples

This directory contains practical examples demonstrating how to use the AI-Powered DevSecOps Pipeline in various scenarios.

---

## Directory Structure

```
examples/
├── basic/                      # Simple, getting-started examples
├── advanced/                   # Advanced usage patterns
└── ci-cd-integration/          # CI/CD platform integrations
```

---

## Basic Examples

### 1. Simple Scan (`basic/simple_scan.py`)

The most basic usage - scan a directory and get results.

```bash
python examples/basic/simple_scan.py
```

**What it demonstrates**:
- Initialize the orchestrator
- Run a basic scan
- Print results to console
- Handle exit codes

**Use case**: Quick local scans, testing the pipeline

---

## Advanced Examples

### 2. Custom ML Model (`advanced/custom_ml_model.py`)

Shows how to use different ML models or fine-tuned versions.

```bash
python examples/advanced/custom_ml_model.py
```

**What it demonstrates**:
- Using alternative transformer models
- Adjusting confidence thresholds
- Analyzing individual files vs. directories
- Accessing model information

**Use case**: Specialized vulnerability detection, research

---

### 3. Train Correlation Model (`advanced/train_correlation_model.py`)

Demonstrates training the alert correlation engine on your own labeled data.

```bash
python examples/advanced/train_correlation_model.py
```

**What it demonstrates**:
- Creating labeled training data
- Training the false positive classifier
- Evaluating model performance
- Continuous learning workflow

**Use case**: Improving detection accuracy over time, customization

---

## CI/CD Integration Examples

### 4. GitLab CI (`ci-cd-integration/gitlab-ci.yml`)

Complete GitLab CI/CD configuration.

```yaml
# Copy to your project
cp examples/ci-cd-integration/gitlab-ci.yml .gitlab-ci.yml
```

**What it demonstrates**:
- Multi-stage pipeline (scan, report, deploy)
- Artifact management
- GPU runner usage (optional)
- Deployment gating
- Metrics publishing

**Use case**: GitLab-based projects

---

### 5. Jenkins Pipeline (`ci-cd-integration/Jenkinsfile`)

Declarative Jenkins pipeline example.

```groovy
// Copy to your project
cp examples/ci-cd-integration/Jenkinsfile ./Jenkinsfile
```

**What it demonstrates**:
- Jenkins declarative pipeline
- Parallel scanning stages
- Quality gates
- HTML report publishing

**Use case**: Jenkins-based projects

---

## Running the Examples

### Prerequisites

```bash
# Install the package
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
pip install bandit semgrep safety
```

### Option 1: Run Directly

```bash
# Basic example
python examples/basic/simple_scan.py

# Advanced examples
python examples/advanced/custom_ml_model.py
python examples/advanced/train_correlation_model.py
```

### Option 2: Using Make

```bash
# Run all examples
make examples

# Run specific example
make example-basic
make example-advanced
```

---

## Example Output

### Simple Scan Output

```
======================================================================
BASIC SECURITY SCAN EXAMPLE
======================================================================

Scanning: /path/to/vulnerable-flask-app

🚀 Starting AI-Powered DevSecOps Pipeline
├─ 🔍 Running SAST Analysis...
│  ├─ Bandit: 8 issues (3 critical, 5 high)
│  └─ Semgrep: 5 issues found
├─ 📋 Running Dependency Scanning...
│  └─ Safety: 3 vulnerabilities found
└─ ✅ Report saved to scan-results/

======================================================================
SCAN RESULTS
======================================================================
Status: REJECTED
Duration: 47.23 seconds

Findings by Severity:
  CRITICAL: 3
  HIGH: 5
  MEDIUM: 2
  LOW: 1

Report saved to: scan-results/security-assessment-report.json

❌ Critical issues found - review required
```

---

## Customization Tips

### 1. Modify Scanner Configuration

```python
# In your example script
orchestrator = DevSecOpsOrchestrator(config_path='custom-config.yaml')
```

### 2. Adjust ML Parameters

```python
analyzer = SemanticCodeAnalyzer(
    model_name="your-org/fine-tuned-model",
    device="cuda",  # Use GPU
    confidence_threshold=0.80  # More strict
)
```

### 3. Custom Policy Enforcement

```python
# Use custom policy file
result = enforce_policies(
    findings,
    policy_path='policies/strict-policy.yaml'
)
```

---

## Creating Your Own Examples

### Template Structure

```python
#!/usr/bin/env python3
"""
Your Example Name
=================

Description of what this example demonstrates.
"""

import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Your imports
from scripts.orchestrate_devsecops import DevSecOpsOrchestrator

def main():
    """Your example code"""
    # Initialize
    orchestrator = DevSecOpsOrchestrator()

    # Do something interesting
    result = orchestrator.execute_full_pipeline('.')

    # Show results
    print(f"Status: {result['status']}")

if __name__ == "__main__":
    main()
```

---

## Additional Resources

- [Main Documentation](../documentation/INSTALLATION.md)
- [API Reference](../documentation/API_REFERENCE.md)
- [Architecture Guide](../documentation/ARCHITECTURE.md)
- [Troubleshooting](../documentation/TROUBLESHOOTING.md)

---

## Contributing Examples

We welcome contributions of new examples! To add an example:

1. Create your example script in the appropriate directory
2. Add clear docstrings explaining what it demonstrates
3. Test it works with current version
4. Update this README
5. Submit a pull request

See [CONTRIBUTING.md](../documentation/CONTRIBUTING.md) for guidelines.

---

## Example Ideas (Contributions Welcome!)

- [ ] Multi-repository scanning
- [ ] Integration with Jira for ticket creation
- [ ] Slack notification example
- [ ] Custom scanner integration
- [ ] Kubernetes deployment with security gates
- [ ] CircleCI integration
- [ ] Azure DevOps pipeline
- [ ] Pre-commit hook example
- [ ] IDE plugin usage

---

**Need Help?** Open an [issue](https://github.com/yourusername/APSCRDP/issues) or check [Discussions](https://github.com/yourusername/APSCRDP/discussions).
