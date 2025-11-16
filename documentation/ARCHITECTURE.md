# Architecture Documentation

## AI-Powered DevSecOps Pipeline - Technical Architecture

This document provides an in-depth technical overview of the system architecture, design patterns, and implementation details.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [ML Model Architecture](#ml-model-architecture)
5. [Security Design](#security-design)
6. [Scalability Considerations](#scalability-considerations)
7. [Design Patterns](#design-patterns)
8. [Technology Stack](#technology-stack)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                             │
│  (Developer pushes code → GitHub → Pipeline → Security Decision)    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │   ORCHESTRATION LAYER        │
              │  - orchestrate_devsecops.py  │
              │  - Configuration Management  │
              │  - State Management          │
              └──────┬──────────┬────────────┘
                     │          │
        ┌────────────▼──┐  ┌───▼──────────────┐
        │  SCANNER LAYER │  │  ML/AI LAYER     │
        └────────┬───────┘  └───┬──────────────┘
                 │              │
     ┌───────────▼──────────────▼────────────┐
     │      AGGREGATION & NORMALIZATION      │
     │    - Report parsing                   │
     │    - Data standardization             │
     │    - Alert enrichment                 │
     └────────────────┬──────────────────────┘
                      │
     ┌────────────────▼──────────────────────┐
     │      ML CORRELATION ENGINE            │
     │    - False positive filtering         │
     │    - Alert deduplication              │
     │    - Priority scoring                 │
     └────────────────┬──────────────────────┘
                      │
     ┌────────────────▼──────────────────────┐
     │      POLICY ENFORCEMENT LAYER         │
     │    - Rule evaluation                  │
     │    - Deployment gating                │
     │    - Compliance checking              │
     └────────────────┬──────────────────────┘
                      │
     ┌────────────────▼──────────────────────┐
     │      REPORTING & OUTPUT LAYER         │
     │    - HTML/JSON generation             │
     │    - Notifications                    │
     │    - Metrics export                   │
     └───────────────────────────────────────┘
```

### Design Principles

1. **Modularity**: Each component is independently testable and replaceable
2. **Extensibility**: New scanners and ML models can be added without core changes
3. **Fault Tolerance**: Pipeline continues even if individual scanners fail
4. **Performance**: Parallel execution where possible, caching for efficiency
5. **Security**: Least privilege, input validation, secure defaults

---

## Component Architecture

### 1. Orchestration Layer

**Purpose**: Coordinates all pipeline activities, manages state, and handles configuration.

**Key Components**:
- `orchestrate_devsecops.py`: Main entry point
- Configuration loader (YAML/ENV)
- State manager
- Error handler

**Design Pattern**: **Facade Pattern**
- Provides simplified interface to complex scanner subsystems
- Manages lifecycle of all components

```python
class DevSecOpsOrchestrator:
    """
    Facade for entire pipeline.
    Responsibilities:
    - Load configuration
    - Initialize scanners
    - Coordinate execution
    - Aggregate results
    - Generate reports
    """
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.scan_results = []

    def execute_full_pipeline(self, target_path):
        # Orchestrate all stages
        self.execute_sast()
        self.execute_dependency_scan()
        self.execute_ml_correlation()
        self.enforce_policies()
        return self.generate_report()
```

### 2. Scanner Layer

**Purpose**: Interface with various security scanning tools.

**Design Pattern**: **Adapter Pattern**
- Each scanner has a consistent interface
- Internal scanner differences are abstracted

```python
class ScannerInterface:
    """Abstract base class for all scanners"""
    def scan(self, target: str) -> ScanResult:
        raise NotImplementedError

    def parse_results(self, raw_output: str) -> List[Alert]:
        raise NotImplementedError

class BanditScanner(ScannerInterface):
    """Adapter for Bandit Python scanner"""
    def scan(self, target: str) -> ScanResult:
        # Bandit-specific implementation
        ...

class SemgrepScanner(ScannerInterface):
    """Adapter for Semgrep multi-language scanner"""
    def scan(self, target: str) -> ScanResult:
        # Semgrep-specific implementation
        ...
```

**Scanners Integrated**:
- **Bandit**: Python SAST
- **Semgrep**: Multi-language pattern matching
- **Safety**: Python dependency checker
- **Trivy**: Container vulnerability scanner
- **Checkov**: IaC security scanner

### 3. ML/AI Layer

**Purpose**: Apply machine learning for intelligent analysis.

**Components**:

#### 3.1 Semantic Code Analyzer

**Architecture**:
```
Input (Source Code)
    ↓
Tokenization (CodeBERT Tokenizer)
    ↓
Embedding Layer (768-dim vectors)
    ↓
Transformer Encoder (12 layers)
    ↓
Classification Head (25 vulnerability classes)
    ↓
Output (Vulnerability predictions with confidence)
```

**Model Details**:
- **Base Model**: microsoft/codebert-base
- **Parameters**: 125M
- **Input**: Source code (max 512 tokens)
- **Output**: 25-class probability distribution
- **Inference Time**: <100ms per file (CPU)

```python
class SemanticCodeAnalyzer:
    """
    Transformer-based vulnerability detection.

    Architecture:
    - Tokenizer: CodeBERT tokenizer (50K vocab)
    - Model: 12-layer transformer (125M params)
    - Head: Linear(768 → 25) classification

    Training (future):
    - Dataset: Security-labeled code snippets
    - Loss: Cross-entropy
    - Optimizer: AdamW
    - Learning rate: 2e-5
    """
    def __init__(self, model_name="microsoft/codebert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=25
        )
```

#### 3.2 Alert Correlation Engine

**Architecture**:
```
Multiple Scanner Alerts
    ↓
Feature Engineering (7 dimensions)
    ↓
┌─────────────────┬─────────────────┐
│ Isolation Forest│ Random Forest   │
│ (Anomaly Detect)│ (FP Classifier) │
└────────┬────────┴────────┬────────┘
         ↓                 ↓
    Anomaly Scores   FP Probabilities
         ↓                 ↓
    ┌────────────────────────┐
    │  DBSCAN Clustering     │
    │  (Deduplication)       │
    └────────┬───────────────┘
             ↓
    Priority Scoring (Weighted)
             ↓
    Grouped by Severity
```

**Feature Engineering**:
```python
Features = {
    'vulnerability_type': one_hot_encoded,
    'severity_score': 0-10 scale,
    'confidence': 0.0-1.0,
    'line_number': int,
    'scanner_agreement': 0.0-1.0,  # Multi-scanner confirmation
    'exploitability_score': CVSS-based,
    'asset_criticality': 1-5 scale,
}
```

**ML Models Used**:
1. **Isolation Forest**: Anomaly detection (unsupervised)
   - contamination=0.05 (5% expected outliers)
   - n_estimators=100

2. **Random Forest**: False positive classification (supervised)
   - n_estimators=100
   - max_depth=10
   - Trained on analyst feedback

3. **DBSCAN**: Alert clustering
   - eps=0.5
   - min_samples=1

**Priority Calculation**:
```
Priority = 0.35 × severity
         + 0.25 × exploitability
         + 0.20 × asset_criticality
         + 0.15 × scanner_agreement
         + 0.05 × (1 - false_positive_likelihood)
```

### 4. Policy Enforcement Layer

**Purpose**: Apply business rules and compliance requirements.

**Design Pattern**: **Strategy Pattern**
- Policies are interchangeable strategies
- Easy to add new policy types

```python
class PolicyStrategy:
    """Abstract policy strategy"""
    def evaluate(self, findings: Dict) -> PolicyResult:
        raise NotImplementedError

class VulnerabilityThresholdPolicy(PolicyStrategy):
    """Policy based on vulnerability counts"""
    def evaluate(self, findings):
        violations = []
        if len(findings['CRITICAL']) > self.max_critical:
            violations.append('Critical threshold exceeded')
        return PolicyResult(approved=len(violations)==0)

class CompliancePolicy(PolicyStrategy):
    """Policy based on compliance frameworks"""
    def evaluate(self, findings):
        # Check OWASP Top 10, CWE Top 25, etc.
        ...
```

### 5. Reporting Layer

**Purpose**: Generate human and machine-readable outputs.

**Formats Supported**:
- HTML (interactive, styled)
- JSON (machine-readable)
- SARIF (GitHub Security integration)
- Markdown (GitHub comments)

---

## Data Flow

### Complete Pipeline Flow

```
1. CODE PUSH
   Developer → Git → GitHub

2. TRIGGER
   GitHub Webhook → GitHub Actions

3. CHECKOUT
   Actions Runner → Clone Repo

4. SCAN PHASE
   Parallel Execution:
   ├── Bandit (Python SAST)
   ├── Semgrep (Multi-lang SAST)
   ├── Safety (Dependency)
   └── Trivy (Container)

5. AGGREGATION
   Parse JSON/SARIF → Normalize → Enrich

6. ML CORRELATION
   Feature Extraction → ML Models → Deduplicate

7. PRIORITIZATION
   Score → Rank → Group by Severity

8. POLICY CHECK
   Evaluate Rules → Approve/Reject

9. REPORTING
   Generate HTML/JSON → Upload Artifacts

10. NOTIFICATION
    GitHub Comment → Email/Slack (if configured)
```

### Data Structures

#### Alert Object
```python
Alert = {
    'id': str,  # Unique identifier
    'type': str,  # Vulnerability type
    'severity': str,  # CRITICAL, HIGH, MEDIUM, LOW
    'file': str,  # File path
    'line': int,  # Line number
    'confidence': float,  # 0.0-1.0
    'reported_by': List[str],  # Scanner names
    'cwe_id': str,  # CWE identifier
    'message': str,  # Description
    'remediation': str,  # Fix suggestion
}
```

#### Scan Result Object
```python
ScanResult = {
    'scanner_name': str,
    'duration_seconds': float,
    'vulnerabilities_found': int,
    'critical_count': int,
    'high_count': int,
    'medium_count': int,
    'low_count': int,
    'report_path': str,
    'success': bool,
}
```

---

## Security Design

### Threat Model

**Assets Protected**:
1. Source code being scanned
2. Scanner configurations
3. ML model weights
4. Scan results and reports

**Threats Mitigated**:
1. **Code Injection**: Input validation on all user inputs
2. **Secrets Leakage**: No hardcoded secrets, env vars used
3. **Privilege Escalation**: Non-root Docker containers
4. **Data Exposure**: Scan results are access-controlled

### Security Controls

1. **Input Validation**:
   - Path traversal prevention
   - Command injection prevention
   - File type validation

2. **Least Privilege**:
   - Docker containers run as non-root
   - GitHub Actions use minimal permissions
   - File system access restricted

3. **Secure Defaults**:
   - TLS for all network communications
   - No debug mode in production
   - Conservative security policies

---

## Scalability Considerations

### Current Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| Max file size | 10 MB | Per file for analysis |
| Max files | 100,000 | Per repository |
| Scan timeout | 30 min | Configurable |
| ML model memory | 2 GB | For CodeBERT |
| Concurrent scans | 4 | Parallel scanners |

### Scaling Strategies

#### Horizontal Scaling
```
Load Balancer
    ↓
┌────────────────────────────┐
│  Scanner Worker Pool       │
│  ┌──────┐ ┌──────┐ ┌──────┐│
│  │Worker│ │Worker│ │Worker││
│  └──────┘ └──────┘ └──────┘│
└────────────────────────────┘
    ↓
Results Queue (Redis)
    ↓
ML Processing Workers
```

#### Optimization Techniques
1. **Caching**: Cache scanner results for unchanged files
2. **Incremental Analysis**: Only scan changed files
3. **Lazy Loading**: Load ML models only when needed
4. **Parallel Execution**: Run independent scanners concurrently

---

## Design Patterns Used

1. **Facade**: `DevSecOpsOrchestrator` simplifies complex subsystems
2. **Adapter**: Scanner interfaces normalize different tools
3. **Strategy**: Policy enforcement uses interchangeable strategies
4. **Factory**: Scanner creation based on configuration
5. **Observer**: Event-driven notifications
6. **Singleton**: Configuration manager (one instance)

---

## Technology Stack

### Core
- **Language**: Python 3.11+
- **ML Framework**: PyTorch 2.0+, Transformers 4.30+
- **ML Libraries**: scikit-learn 1.3+, pandas 2.0+

### Scanners
- **Bandit**: Python security linting
- **Semgrep**: Multi-language SAST
- **Safety**: Python dependency checker
- **Trivy**: Container scanner
- **Checkov**: IaC scanner

### Infrastructure
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, docker-compose
- **Orchestration**: Kubernetes (optional)
- **Monitoring**: Prometheus, Grafana

### Storage
- **Results**: JSON files, SARIF format
- **Models**: HuggingFace Hub
- **Artifacts**: GitHub Actions artifacts, S3 (optional)

---

## Performance Characteristics

### Benchmarks

**Single File Analysis**:
- Bandit: ~50ms
- Semgrep: ~100ms
- CodeBERT: ~80ms (CPU), ~20ms (GPU)

**Full Repository Scan (1000 files)**:
- SAST Phase: ~45 seconds
- Dependency Scan: ~15 seconds
- ML Correlation: ~5 seconds
- **Total**: <2 minutes

### Bottlenecks

1. **ML Model Loading**: ~2 seconds initial load (one-time)
2. **Large Files**: Files >1MB slow down analysis
3. **Network I/O**: Downloading dependencies for first scan

---

## Future Architecture Enhancements

### Planned Improvements

1. **Microservices Architecture**:
   - Split into dedicated services (Scanner Service, ML Service, Report Service)
   - API Gateway for unified interface
   - Message queue for async processing

2. **Distributed ML**:
   - Model serving with TensorFlow Serving or TorchServe
   - Distributed inference for large codebases
   - A/B testing for model improvements

3. **Real-Time Scanning**:
   - WebSocket connections for live results
   - Streaming analysis as code is written (IDE plugin)
   - Hot-reload for configuration changes

---

## References

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

**Last Updated**: 2025-11-16
**Maintained By**: APSCRDP Team
**Version**: 1.0.0
