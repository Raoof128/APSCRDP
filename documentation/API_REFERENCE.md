# API Reference

Complete API documentation for integrating with the AI-Powered DevSecOps Pipeline.

## Table of Contents

1. [Python API](#python-api)
2. [Command-Line Interface](#command-line-interface)
3. [GitHub Actions Integration](#github-actions-integration)
4. [REST API (Future)](#rest-api)
5. [Examples](#examples)

---

## Python API

### Semantic Code Analyzer

```python
from ml_models.semantic_code_analyzer import SemanticCodeAnalyzer

# Initialize
analyzer = SemanticCodeAnalyzer(
    model_name="microsoft/codebert-base",
    device="cuda"  # or "cpu"
)

# Analyze code snippet
vulnerabilities = analyzer.analyze_code_snippet(
    code="SELECT * FROM users WHERE id = '" + user_id + "'",
    language="python",
    file_path="app.py",
    confidence_threshold=0.75
)

# Process results
for vuln in vulnerabilities:
    print(f"{vuln.severity}: {vuln.vulnerability_type}")
    print(f"  File: {vuln.file_path}:{vuln.line_number}")
    print(f"  Confidence: {vuln.ml_confidence:.2%}")
    print(f"  CWE: {vuln.cwe_id}")
    print(f"  Fix: {vuln.remediation}")
```

#### Methods

##### `__init__(model_name, device)`
Initialize the semantic analyzer.

**Parameters:**
- `model_name` (str): HuggingFace model identifier
- `device` (str, optional): 'cuda', 'cpu', or None for auto-detect

##### `analyze_code_snippet(code, language, file_path, confidence_threshold)`
Analyze a code snippet for vulnerabilities.

**Parameters:**
- `code` (str): Source code to analyze
- `language` (str): Programming language
- `file_path` (str): Path to source file
- `confidence_threshold` (float): Minimum confidence (0.0-1.0)

**Returns:**
- List[CodeVulnerability]: Detected vulnerabilities

##### `analyze_file(file_path, language, confidence_threshold)`
Analyze entire file.

**Parameters:**
- `file_path` (str): Path to file
- `language` (str): Programming language
- `confidence_threshold` (float): Minimum confidence

**Returns:**
- List[CodeVulnerability]: Detected vulnerabilities

---

### Alert Correlation Engine

```python
from ml_models.alert_correlation_engine import AlertCorrelationEngine

# Initialize
engine = AlertCorrelationEngine(contamination=0.05)

# Correlate alerts
raw_alerts = [
    {
        'type': 'SQL_INJECTION',
        'severity': 'CRITICAL',
        'file': 'app.py',
        'line': 42,
        'confidence': 0.95,
        'reported_by': ['Bandit', 'Semgrep']
    },
    # ... more alerts
]

correlated = engine.correlate_and_prioritize(
    raw_alerts,
    min_priority_score=0.0
)

# Results grouped by severity
print(f"Critical: {len(correlated['CRITICAL'])}")
print(f"High: {len(correlated['HIGH'])}")

# Get statistics
stats = engine.get_statistics(correlated)
print(f"Total: {stats['total_alerts']}")
print(f"FP filtered: {correlated['false_positives_filtered']}")
```

#### Methods

##### `__init__(contamination)`
Initialize correlation engine.

**Parameters:**
- `contamination` (float): Expected proportion of outliers (false positives)

##### `correlate_and_prioritize(alerts, min_priority_score)`
Correlate and prioritize alerts.

**Parameters:**
- `alerts` (List[Dict]): Raw alerts from scanners
- `min_priority_score` (float): Minimum priority to include

**Returns:**
- Dict[str, List[Dict]]: Alerts grouped by severity

##### `train_on_feedback(labeled_alerts, save_model_path)`
Train classifier on analyst feedback.

**Parameters:**
- `labeled_alerts` (List[Dict]): Alerts with `is_false_positive` labels
- `save_model_path` (str, optional): Path to save model

##### `get_statistics(results)`
Get summary statistics.

**Parameters:**
- `results` (Dict): Correlated results

**Returns:**
- Dict: Statistics (total, by severity, etc.)

---

## Command-Line Interface

### Main Orchestrator

```bash
python scripts/orchestrate_devsecops.py \
  --target /path/to/code \
  --config config.yaml \
  --output results/
```

**Options:**
- `--target PATH`: Code directory to scan (default: current directory)
- `--config FILE`: Configuration file (YAML)
- `--output DIR`: Output directory for reports (default: scan-results/)

**Exit Codes:**
- `0`: Success (deployment approved)
- `1`: Failure (deployment rejected or error)

### Alert Correlation

```bash
python scripts/run_correlation.py \
  --sast-dir sast-reports/ \
  --dependency-dir dep-reports/ \
  --container-dir container-reports/ \
  --output consolidated.json
```

### Report Generation

```bash
python scripts/generate_security_report.py \
  --findings consolidated.json \
  --format html \
  --output report.html
```

**Formats:**
- `html`: Interactive HTML report
- `json`: Machine-readable JSON

### Policy Enforcement

```bash
python scripts/policy_enforcement.py \
  --findings consolidated.json \
  --policy policies/deployment-gate-policy.yaml \
  --fail-on critical
```

**Fail Thresholds:**
- `critical`: Fail only on critical violations
- `high`: Fail on critical or high
- `medium`: Fail on critical, high, or medium
- `any`: Fail on any violation

---

## GitHub Actions Integration

### Basic Workflow

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run DevSecOps Pipeline
        run: |
          pip install -r requirements.txt
          python scripts/orchestrate_devsecops.py \
            --target . \
            --output security-results

      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security-results/
```

### With Policy Enforcement

```yaml
- name: Enforce Security Policy
  run: |
    python scripts/policy_enforcement.py \
      --findings security-results/consolidated.json \
      --policy policies/deployment-gate-policy.yaml \
      --fail-on critical
```

---

## REST API (Future Enhancement)

Planned REST API for remote scanning and integration.

### Endpoints (Planned)

#### POST /api/v1/scan
Submit code for scanning.

**Request:**
```json
{
  "code": "def get_user(id): ...",
  "language": "python",
  "options": {
    "confidence_threshold": 0.75
  }
}
```

**Response:**
```json
{
  "scan_id": "abc123",
  "status": "completed",
  "vulnerabilities": [
    {
      "type": "SQL_INJECTION",
      "severity": "CRITICAL",
      "line": 42,
      "confidence": 0.95
    }
  ]
}
```

#### GET /api/v1/scan/{scan_id}
Get scan results.

---

## Examples

### Example 1: Scan Python Project

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.orchestrate_devsecops import DevSecOpsOrchestrator

# Initialize
orchestrator = DevSecOpsOrchestrator()

# Run full pipeline
result = orchestrator.execute_full_pipeline(
    target_path="/path/to/project"
)

# Check result
if result['status'] == 'SUCCESS':
    print("✅ Deployment approved")
else:
    print("❌ Deployment rejected")
    print(f"Violations: {result['policy_result']}")
```

### Example 2: Custom ML Model

```python
from ml_models.semantic_code_analyzer import SemanticCodeAnalyzer

# Use custom model
analyzer = SemanticCodeAnalyzer(
    model_name="your-org/custom-security-model",
    device="cuda"
)

# Analyze with lower threshold
vulnerabilities = analyzer.analyze_file(
    "vulnerable_app.py",
    language="python",
    confidence_threshold=0.60  # Lower threshold
)
```

### Example 3: Train Correlation Model

```python
from ml_models.alert_correlation_engine import AlertCorrelationEngine

# Load historical alerts with labels
import json
with open('labeled_alerts.json') as f:
    labeled_alerts = json.load(f)

# Train model
engine = AlertCorrelationEngine()
engine.train_on_feedback(
    labeled_alerts,
    save_model_path='models/custom_classifier.pkl'
)

# Use trained model
correlated = engine.correlate_and_prioritize(new_alerts)
```

---

## Integration Examples

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Security Scan') {
            steps {
                sh '''
                    python scripts/orchestrate_devsecops.py \
                        --target . \
                        --output ${WORKSPACE}/security-results
                '''
            }
        }
        stage('Policy Check') {
            steps {
                sh '''
                    python scripts/policy_enforcement.py \
                        --findings security-results/consolidated.json \
                        --policy policies/deployment-gate-policy.yaml \
                        --fail-on critical
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'security-results/**'
        }
    }
}
```

### GitLab CI

```yaml
security_scan:
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python scripts/orchestrate_devsecops.py --target . --output results/
  artifacts:
    paths:
      - results/
    reports:
      sast: results/consolidated.json
```

---

## Error Handling

All functions raise standard Python exceptions:

```python
try:
    vulnerabilities = analyzer.analyze_file('app.py')
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Analysis failed: {e}")
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for API extension guidelines.

---

**Last Updated**: November 2025
