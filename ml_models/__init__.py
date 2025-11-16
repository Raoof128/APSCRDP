"""
AI-Powered DevSecOps Pipeline - ML Models Package

This package contains machine learning models for security analysis:
- Semantic Code Analyzer: CodeBERT-based vulnerability detection
- Alert Correlation Engine: ML-based false positive reduction
"""

__version__ = "1.0.0"
__author__ = "APSCRDP Team"

try:
    from .semantic_code_analyzer import SemanticCodeAnalyzer, CodeVulnerability
    from .alert_correlation_engine import AlertCorrelationEngine
except ImportError:
    # Fallback for when package is not installed
    pass

__all__ = [
    "SemanticCodeAnalyzer",
    "CodeVulnerability",
    "AlertCorrelationEngine",
]
