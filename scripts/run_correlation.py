#!/usr/bin/env python3
"""
Script to run ML alert correlation on scanner outputs
Called by GitHub Actions workflow
"""

import json
import argparse
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_scanner_reports(directory: Path) -> list:
    """Load all JSON reports from a directory"""
    alerts = []

    if not directory.exists():
        logger.warning(f"Directory not found: {directory}")
        return alerts

    for json_file in directory.rglob('*.json'):
        try:
            with open(json_file) as f:
                data = json.load(f)
                logger.info(f"Loaded {json_file.name}")

                # Parse based on file name patterns
                if 'bandit' in json_file.name:
                    alerts.extend(parse_bandit(data))
                elif 'safety' in json_file.name:
                    alerts.extend(parse_safety(data))
                elif 'semgrep' in json_file.name:
                    alerts.extend(parse_semgrep(data))

        except Exception as e:
            logger.error(f"Error loading {json_file}: {e}")

    return alerts


def parse_bandit(data: dict) -> list:
    """Parse Bandit report format"""
    alerts = []
    for result in data.get('results', []):
        alerts.append({
            'type': result.get('test_id', 'UNKNOWN'),
            'severity': result.get('issue_severity', 'MEDIUM'),
            'file': result.get('filename', ''),
            'line': result.get('line_number', 0),
            'confidence': 0.8,
            'reported_by': ['Bandit'],
            'cwe': result.get('cwe', {}).get('id', '') if isinstance(result.get('cwe'), dict) else '',
            'message': result.get('issue_text', '')
        })
    return alerts


def parse_safety(data: dict) -> list:
    """Parse Safety report format"""
    alerts = []
    if isinstance(data, list):
        for vuln in data:
            alerts.append({
                'type': 'VULNERABLE_DEPENDENCY',
                'severity': 'HIGH',
                'file': vuln.get('package', ''),
                'line': 0,
                'confidence': 0.9,
                'reported_by': ['Safety'],
                'message': vuln.get('advisory', '')
            })
    return alerts


def parse_semgrep(data: dict) -> list:
    """Parse Semgrep report format"""
    alerts = []
    for result in data.get('results', []):
        alerts.append({
            'type': result.get('check_id', 'UNKNOWN').split('.')[-1],
            'severity': 'HIGH',
            'file': result.get('path', ''),
            'line': result.get('start', {}).get('line', 0),
            'confidence': 0.85,
            'reported_by': ['Semgrep'],
            'message': result.get('extra', {}).get('message', '')
        })
    return alerts


def main():
    parser = argparse.ArgumentParser(description='Run ML alert correlation')
    parser.add_argument('--sast-dir', type=Path, help='SAST reports directory')
    parser.add_argument('--dependency-dir', type=Path, help='Dependency reports directory')
    parser.add_argument('--container-dir', type=Path, help='Container reports directory')
    parser.add_argument('--output', type=Path, required=True, help='Output file')

    args = parser.parse_args()

    # Collect all alerts
    all_alerts = []

    if args.sast_dir:
        all_alerts.extend(load_scanner_reports(args.sast_dir))
    if args.dependency_dir:
        all_alerts.extend(load_scanner_reports(args.dependency_dir))
    if args.container_dir:
        all_alerts.extend(load_scanner_reports(args.container_dir))

    logger.info(f"Total raw alerts: {len(all_alerts)}")

    if not all_alerts:
        logger.warning("No alerts found, creating empty report")
        output = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': [],
            'INFO': [],
            'false_positives_filtered': 0,
            'total_raw_alerts': 0
        }
    else:
        # Try to run ML correlation
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from ml_models.alert_correlation_engine import AlertCorrelationEngine

            engine = AlertCorrelationEngine()
            output = engine.correlate_and_prioritize(all_alerts)

            # Add metadata
            stats = engine.get_statistics(output)
            output['false_positives_filtered'] = len(all_alerts) - stats['total_alerts']
            output['total_raw_alerts'] = len(all_alerts)

            logger.info(f"Correlated alerts: {stats['total_alerts']}")
            logger.info(f"False positives filtered: {output['false_positives_filtered']}")

        except ImportError as e:
            logger.error(f"ML modules not available: {e}")
            # Fallback: simple severity grouping
            output = group_by_severity(all_alerts)

    # Save results
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)

    logger.info(f"Results saved to {args.output}")


def group_by_severity(alerts: list) -> dict:
    """Simple fallback grouping by severity"""
    grouped = {
        'CRITICAL': [],
        'HIGH': [],
        'MEDIUM': [],
        'LOW': [],
        'INFO': []
    }

    for alert in alerts:
        severity = alert.get('severity', 'MEDIUM').upper()
        if severity in grouped:
            grouped[severity].append(alert)
        else:
            grouped['MEDIUM'].append(alert)

    grouped['false_positives_filtered'] = 0
    grouped['total_raw_alerts'] = len(alerts)

    return grouped


if __name__ == '__main__':
    main()
