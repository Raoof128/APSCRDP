#!/usr/bin/env python3
"""
Policy enforcement and deployment gating
"""

import json
import argparse
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_POLICY = {
    'max_critical_vulnerabilities': 0,
    'max_high_vulnerabilities': 5,
    'max_medium_vulnerabilities': 20,
    'block_on_policy_violation': True,
    'allowed_cwe_exceptions': [],  # CWEs that are acceptable
}


def load_policy(policy_file: Path) -> dict:
    """Load policy configuration"""
    if not policy_file or not policy_file.exists():
        logger.warning(f"Policy file not found, using defaults")
        return DEFAULT_POLICY

    try:
        import yaml
        with open(policy_file) as f:
            policy = yaml.safe_load(f)
            return {**DEFAULT_POLICY, **policy}
    except ImportError:
        logger.warning("PyYAML not available, using defaults")
        return DEFAULT_POLICY
    except Exception as e:
        logger.error(f"Failed to load policy: {e}")
        return DEFAULT_POLICY


def enforce_policy(findings: dict, policy: dict, fail_on: str = 'critical') -> bool:
    """
    Enforce security policy on findings.

    Args:
        findings: Security findings from correlation engine
        policy: Policy configuration
        fail_on: Fail threshold ('critical', 'high', 'medium', 'any')

    Returns:
        True if policy passes, False otherwise
    """
    critical_count = len(findings.get('CRITICAL', []))
    high_count = len(findings.get('HIGH', []))
    medium_count = len(findings.get('MEDIUM', []))

    max_critical = policy.get('max_critical_vulnerabilities', 0)
    max_high = policy.get('max_high_vulnerabilities', 5)
    max_medium = policy.get('max_medium_vulnerabilities', 20)

    violations = []

    # Check critical threshold
    if critical_count > max_critical:
        violations.append(f"Critical vulnerabilities: {critical_count} > {max_critical}")

    # Check high threshold
    if high_count > max_high:
        violations.append(f"High vulnerabilities: {high_count} > {max_high}")

    # Check medium threshold
    if medium_count > max_medium:
        violations.append(f"Medium vulnerabilities: {medium_count} > {max_medium}")

    # Determine if we should fail based on fail_on parameter
    should_fail = False

    if fail_on == 'critical' and critical_count > max_critical:
        should_fail = True
    elif fail_on == 'high' and (critical_count > max_critical or high_count > max_high):
        should_fail = True
    elif fail_on == 'medium' and (critical_count > max_critical or high_count > max_high or medium_count > max_medium):
        should_fail = True
    elif fail_on == 'any' and violations:
        should_fail = True

    # Print results
    print("\n" + "="*70)
    print("POLICY ENFORCEMENT RESULTS")
    print("="*70)
    print(f"\nSeverity Counts:")
    print(f"  Critical: {critical_count} (max: {max_critical})")
    print(f"  High:     {high_count} (max: {max_high})")
    print(f"  Medium:   {medium_count} (max: {max_medium})")
    print(f"\nFail Threshold: {fail_on}")

    if violations:
        print(f"\n⚠️  Policy Violations:")
        for v in violations:
            print(f"  - {v}")
    else:
        print("\n✅ All policy checks passed")

    if should_fail:
        print("\n❌ DEPLOYMENT REJECTED")
        print("="*70 + "\n")
        return False
    else:
        print("\n✅ DEPLOYMENT APPROVED")
        print("="*70 + "\n")
        return True


def main():
    parser = argparse.ArgumentParser(description='Enforce security policies')
    parser.add_argument('--findings', type=Path, required=True, help='Findings JSON file')
    parser.add_argument('--policy', type=Path, help='Policy YAML file')
    parser.add_argument(
        '--fail-on',
        choices=['critical', 'high', 'medium', 'any'],
        default='critical',
        help='Threshold for failing the build'
    )

    args = parser.parse_args()

    # Load findings
    try:
        with open(args.findings) as f:
            findings = json.load(f)
    except FileNotFoundError:
        logger.error(f"Findings file not found: {args.findings}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to load findings: {e}")
        sys.exit(1)

    # Load policy
    policy = load_policy(args.policy)

    # Enforce policy
    passed = enforce_policy(findings, policy, args.fail_on)

    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
