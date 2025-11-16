#!/usr/bin/env python3
"""
Custom ML Model Example
=======================

This example shows how to use custom ML models or fine-tuned versions
for specialized vulnerability detection.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from ml_models.semantic_code_analyzer import SemanticCodeAnalyzer


def analyze_with_custom_model():
    """Example using a custom/fine-tuned model"""
    print("=" * 70)
    print("CUSTOM ML MODEL EXAMPLE")
    print("=" * 70)
    print()

    # Example 1: Use a different base model
    print("1. Using alternative model...")
    analyzer = SemanticCodeAnalyzer(
        model_name="microsoft/graphcodebert-base",  # Different model
        device="cpu"  # Force CPU usage
    )

    # Example code to analyze
    vulnerable_code = '''
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)  # SQL Injection vulnerability
    return cursor.fetchone()
'''

    print("Analyzing code...")
    vulnerabilities = analyzer.analyze_code_snippet(
        code=vulnerable_code,
        language="python",
        file_path="example.py",
        confidence_threshold=0.70  # Lower threshold for more findings
    )

    print(f"\nFound {len(vulnerabilities)} vulnerabilities:\n")
    for vuln in vulnerabilities:
        print(f"  [{vuln.severity}] {vuln.vulnerability_type}")
        print(f"    Line: {vuln.line_number}")
        print(f"    Confidence: {vuln.ml_confidence:.2%}")
        print(f"    CWE: {vuln.cwe_id}")
        print(f"    Remediation: {vuln.remediation}")
        print()

    # Example 2: Analyze actual file
    print("\n2. Analyzing file...")
    test_file = project_root / "sample-apps" / "vulnerable-flask-app" / "app.py"

    if test_file.exists():
        vulnerabilities = analyzer.analyze_file(
            str(test_file),
            language="python",
            confidence_threshold=0.75
        )

        print(f"Found {len(vulnerabilities)} vulnerabilities in {test_file.name}")

        # Group by severity
        by_severity = {}
        for vuln in vulnerabilities:
            by_severity.setdefault(vuln.severity, []).append(vuln)

        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in by_severity:
                print(f"\n  {severity}:")
                for vuln in by_severity[severity]:
                    print(f"    - {vuln.vulnerability_type} (line {vuln.line_number})")

    # Example 3: Model information
    print("\n3. Model Information:")
    info = analyzer.get_model_info()
    print(f"  Device: {info['device']}")
    print(f"  Number of labels: {info['num_labels']}")
    print(f"  Model type: {info['model_type']}")

    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    analyze_with_custom_model()
