#!/usr/bin/env python3
"""
Simple Scan Example
===================

This example demonstrates the most basic usage of the DevSecOps pipeline.
Scans a single directory and outputs results to console.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.orchestrate_devsecops import DevSecOpsOrchestrator


def main():
    """Run a basic security scan"""
    print("=" * 70)
    print("BASIC SECURITY SCAN EXAMPLE")
    print("=" * 70)
    print()

    # Initialize orchestrator with default configuration
    orchestrator = DevSecOpsOrchestrator()

    # Scan the vulnerable sample application
    target_path = project_root / "sample-apps" / "vulnerable-flask-app"

    print(f"Scanning: {target_path}")
    print()

    # Execute the pipeline
    result = orchestrator.execute_full_pipeline(str(target_path))

    # Print results
    print("\n" + "=" * 70)
    print("SCAN RESULTS")
    print("=" * 70)
    print(f"Status: {result['status']}")
    print(f"Duration: {result['duration_seconds']:.2f} seconds")
    print()

    # Print findings summary
    findings = result.get('findings', {})
    print("Findings by Severity:")
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = len(findings.get(severity, []))
        print(f"  {severity}: {count}")

    print()
    print(f"Report saved to: {result.get('report_path')}")
    print()

    # Exit with appropriate code
    if result['status'] == 'SUCCESS':
        print("✅ No critical issues found!")
        return 0
    else:
        print("❌ Critical issues found - review required")
        return 1


if __name__ == "__main__":
    sys.exit(main())
