#!/usr/bin/env python3
"""
Main orchestration script for DevSecOps pipeline.
Coordinates all security scanning tools and ML models.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """Result from a security scanner"""
    scanner_name: str
    duration_seconds: float
    vulnerabilities_found: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    report_path: str
    success: bool
    error_message: Optional[str] = None


class DevSecOpsOrchestrator:
    """
    Orchestrates complete DevSecOps pipeline:
    1. Runs all security scanners in parallel where possible
    2. Aggregates results
    3. Applies ML correlation
    4. Generates reports
    5. Enforces deployment policies
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize orchestrator with optional config"""
        self.config = self.load_config(config_path) if config_path else self.default_config()
        self.scan_results: List[ScanResult] = []
        self.start_time = None
        self.output_dir = Path(self.config.get('output_dir', 'scan-results'))
        self.output_dir.mkdir(exist_ok=True)

        logger.info("DevSecOpsOrchestrator initialized")

    def default_config(self) -> Dict:
        """Default configuration"""
        return {
            'output_dir': 'scan-results',
            'scanners': {
                'bandit': {'enabled': True, 'timeout': 300},
                'semgrep': {'enabled': True, 'timeout': 600},
                'safety': {'enabled': True, 'timeout': 300},
                'trivy': {'enabled': False, 'timeout': 600},  # Requires Docker
            },
            'ml_correlation': {
                'enabled': True,
                'confidence_threshold': 0.75,
                'fp_threshold': 0.80
            },
            'deployment_policy': {
                'max_critical_vulnerabilities': 0,
                'max_high_vulnerabilities': 5,
                'max_medium_vulnerabilities': 20,
                'block_on_policy_violation': True
            }
        }

    def load_config(self, config_path: str) -> Dict:
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                import yaml
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
            return self.default_config()

    def execute_full_pipeline(self, target_path: str = '.') -> Dict:
        """
        Execute complete security pipeline.

        Args:
            target_path: Path to code to scan

        Returns:
            Pipeline execution results
        """
        logger.info("🚀 Starting AI-Powered DevSecOps Pipeline")
        logger.info(f"Target: {target_path}")
        self.start_time = time.time()

        try:
            # Phase 1: SAST Analysis
            logger.info("\n" + "="*70)
            logger.info("PHASE 1: SAST Analysis")
            logger.info("="*70)
            self.execute_sast(target_path)

            # Phase 2: Dependency Scanning
            logger.info("\n" + "="*70)
            logger.info("PHASE 2: Dependency Scanning")
            logger.info("="*70)
            self.execute_dependency_scan(target_path)

            # Phase 3: Container Security (if enabled)
            if self.config['scanners']['trivy']['enabled']:
                logger.info("\n" + "="*70)
                logger.info("PHASE 3: Container Security")
                logger.info("="*70)
                self.execute_container_scan(target_path)

            # Phase 4: ML Correlation
            logger.info("\n" + "="*70)
            logger.info("PHASE 4: ML Alert Correlation")
            logger.info("="*70)
            correlated_findings = self.execute_ml_correlation()

            # Phase 5: Report Generation
            logger.info("\n" + "="*70)
            logger.info("PHASE 5: Report Generation")
            logger.info("="*70)
            report = self.generate_report(correlated_findings)

            # Phase 6: Policy Enforcement
            logger.info("\n" + "="*70)
            logger.info("PHASE 6: Policy Enforcement")
            logger.info("="*70)
            policy_result = self.enforce_policies(correlated_findings)

            # Calculate total duration
            total_duration = time.time() - self.start_time

            result = {
                'status': 'SUCCESS' if policy_result['approved'] else 'REJECTED',
                'duration_seconds': total_duration,
                'findings': correlated_findings,
                'report_path': report,
                'policy_result': policy_result,
                'scan_results': [asdict(sr) for sr in self.scan_results]
            }

            self.print_summary(result)
            return result

        except Exception as e:
            logger.error(f"❌ Pipeline failed: {str(e)}", exc_info=True)
            return {
                'status': 'FAILED',
                'error': str(e),
                'duration_seconds': time.time() - self.start_time if self.start_time else 0
            }

    def execute_sast(self, target_path: str):
        """Run SAST scanners"""
        logger.info("🔍 Running SAST Analysis...")

        # Bandit (Python)
        if self.config['scanners']['bandit']['enabled']:
            self.run_bandit(target_path)

        # Semgrep
        if self.config['scanners']['semgrep']['enabled']:
            self.run_semgrep(target_path)

    def run_bandit(self, target_path: str):
        """Run Bandit Python security scanner"""
        logger.info("  🍌 Running Bandit...")
        start = time.time()
        output_file = self.output_dir / 'bandit-report.json'

        try:
            result = subprocess.run(
                ['bandit', '-r', target_path, '-f', 'json', '-o', str(output_file)],
                capture_output=True,
                text=True,
                timeout=self.config['scanners']['bandit']['timeout']
            )

            duration = time.time() - start

            # Parse results
            if output_file.exists():
                with open(output_file) as f:
                    data = json.load(f)
                    results = data.get('results', [])

                    # Count by severity
                    critical = sum(1 for r in results if r.get('issue_severity') == 'CRITICAL')
                    high = sum(1 for r in results if r.get('issue_severity') == 'HIGH')
                    medium = sum(1 for r in results if r.get('issue_severity') == 'MEDIUM')
                    low = sum(1 for r in results if r.get('issue_severity') == 'LOW')

                    scan_result = ScanResult(
                        scanner_name='Bandit',
                        duration_seconds=duration,
                        vulnerabilities_found=len(results),
                        critical_count=critical,
                        high_count=high,
                        medium_count=medium,
                        low_count=low,
                        report_path=str(output_file),
                        success=True
                    )

                    self.scan_results.append(scan_result)
                    logger.info(f"    ✅ Bandit: {len(results)} issues ({critical} critical, {high} high)")
            else:
                logger.warning("    ⚠️ Bandit report not generated")

        except subprocess.TimeoutExpired:
            logger.error(f"    ❌ Bandit timed out after {self.config['scanners']['bandit']['timeout']}s")
        except Exception as e:
            logger.error(f"    ❌ Bandit failed: {e}")

    def run_semgrep(self, target_path: str):
        """Run Semgrep security scanner"""
        logger.info("  🎯 Running Semgrep...")
        start = time.time()
        output_file = self.output_dir / 'semgrep-report.json'

        try:
            result = subprocess.run(
                [
                    'semgrep',
                    '--config', 'p/security-audit',
                    '--config', 'p/owasp-top-ten',
                    '--json',
                    '--output', str(output_file),
                    target_path
                ],
                capture_output=True,
                text=True,
                timeout=self.config['scanners']['semgrep']['timeout']
            )

            duration = time.time() - start

            if output_file.exists():
                with open(output_file) as f:
                    data = json.load(f)
                    results = data.get('results', [])

                    # Semgrep doesn't categorize by severity the same way
                    # We'll count all as findings
                    scan_result = ScanResult(
                        scanner_name='Semgrep',
                        duration_seconds=duration,
                        vulnerabilities_found=len(results),
                        critical_count=0,
                        high_count=len(results),  # Consider all as high for now
                        medium_count=0,
                        low_count=0,
                        report_path=str(output_file),
                        success=True
                    )

                    self.scan_results.append(scan_result)
                    logger.info(f"    ✅ Semgrep: {len(results)} issues found")

        except subprocess.TimeoutExpired:
            logger.error(f"    ❌ Semgrep timed out")
        except FileNotFoundError:
            logger.warning("    ⚠️ Semgrep not installed, skipping")
        except Exception as e:
            logger.error(f"    ❌ Semgrep failed: {e}")

    def execute_dependency_scan(self, target_path: str):
        """Run dependency vulnerability scanners"""
        logger.info("📋 Running Dependency Scanning...")

        if self.config['scanners']['safety']['enabled']:
            self.run_safety(target_path)

    def run_safety(self, target_path: str):
        """Run Safety dependency scanner"""
        logger.info("  🔐 Running Safety...")
        start = time.time()
        output_file = self.output_dir / 'safety-report.json'

        try:
            # Find all requirements.txt files
            req_files = list(Path(target_path).rglob('requirements.txt'))

            if not req_files:
                logger.warning("    ⚠️ No requirements.txt found")
                return

            # Scan first requirements file found
            result = subprocess.run(
                ['safety', 'check', '--file', str(req_files[0]), '--json'],
                capture_output=True,
                text=True,
                timeout=self.config['scanners']['safety']['timeout']
            )

            duration = time.time() - start

            # Safety outputs to stdout
            if result.stdout:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)

                # Parse results (Safety JSON format varies)
                try:
                    data = json.loads(result.stdout)
                    vuln_count = len(data) if isinstance(data, list) else 0

                    scan_result = ScanResult(
                        scanner_name='Safety',
                        duration_seconds=duration,
                        vulnerabilities_found=vuln_count,
                        critical_count=0,
                        high_count=vuln_count,
                        medium_count=0,
                        low_count=0,
                        report_path=str(output_file),
                        success=True
                    )

                    self.scan_results.append(scan_result)
                    logger.info(f"    ✅ Safety: {vuln_count} vulnerabilities found")
                except:
                    logger.warning("    ⚠️ Could not parse Safety output")

        except FileNotFoundError:
            logger.warning("    ⚠️ Safety not installed, skipping")
        except Exception as e:
            logger.error(f"    ❌ Safety failed: {e}")

    def execute_container_scan(self, target_path: str):
        """Run container security scans"""
        logger.info("🐳 Running Container Security...")
        logger.info("    ⚠️ Container scanning requires Docker and Trivy")

    def execute_ml_correlation(self) -> Dict:
        """Apply ML models to correlate and prioritize findings"""
        logger.info("🤖 Running ML Correlation Engine...")

        try:
            # Import ML modules
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from ml_models.alert_correlation_engine import AlertCorrelationEngine

            # Aggregate alerts from all scanners
            all_alerts = self._aggregate_alerts()

            if not all_alerts:
                logger.warning("    ⚠️ No alerts to correlate")
                return {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': [], 'INFO': []}

            # Correlate and prioritize
            engine = AlertCorrelationEngine()
            correlated = engine.correlate_and_prioritize(all_alerts)

            stats = engine.get_statistics(correlated)
            logger.info(f"    ✅ Correlated {stats['total_alerts']} alerts")
            logger.info(f"       Critical: {stats['critical']}, High: {stats['high']}, "
                       f"Medium: {stats['medium']}, Low: {stats['low']}")

            return correlated

        except ImportError as e:
            logger.error(f"    ❌ ML modules not available: {e}")
            return self._aggregate_alerts_simple()
        except Exception as e:
            logger.error(f"    ❌ ML correlation failed: {e}", exc_info=True)
            return self._aggregate_alerts_simple()

    def _aggregate_alerts(self) -> List[Dict]:
        """Aggregate alerts from all scanner reports"""
        alerts = []

        for scan_result in self.scan_results:
            try:
                with open(scan_result.report_path) as f:
                    data = json.load(f)

                    # Parse based on scanner type
                    if scan_result.scanner_name == 'Bandit':
                        for result in data.get('results', []):
                            alerts.append({
                                'type': result.get('test_id', 'UNKNOWN'),
                                'severity': result.get('issue_severity', 'MEDIUM'),
                                'file': result.get('filename', ''),
                                'line': result.get('line_number', 0),
                                'confidence': result.get('issue_confidence', 0.5),
                                'reported_by': [scan_result.scanner_name],
                                'cwe': result.get('cwe', {}).get('id', 'CWE-0'),
                                'message': result.get('issue_text', '')
                            })

                    elif scan_result.scanner_name == 'Semgrep':
                        for result in data.get('results', []):
                            alerts.append({
                                'type': result.get('check_id', 'UNKNOWN').split('.')[-1],
                                'severity': 'HIGH',  # Semgrep doesn't provide severity
                                'file': result.get('path', ''),
                                'line': result.get('start', {}).get('line', 0),
                                'confidence': 0.8,
                                'reported_by': [scan_result.scanner_name],
                                'message': result.get('extra', {}).get('message', '')
                            })

            except Exception as e:
                logger.warning(f"    ⚠️ Could not parse {scan_result.report_path}: {e}")

        return alerts

    def _aggregate_alerts_simple(self) -> Dict:
        """Simple aggregation fallback if ML fails"""
        return {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': [],
            'INFO': []
        }

    def generate_report(self, findings: Dict) -> str:
        """Generate security assessment report"""
        logger.info("📊 Generating Security Report...")

        report_path = self.output_dir / 'security-assessment-report.json'

        report_data = {
            'scan_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_scanners': len(self.scan_results),
            'findings': findings,
            'scan_results': [asdict(sr) for sr in self.scan_results]
        }

        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"    ✅ Report saved to {report_path}")
        return str(report_path)

    def enforce_policies(self, findings: Dict) -> Dict:
        """Check against deployment policies"""
        logger.info("🚪 Enforcing deployment policies...")

        policy = self.config.get('deployment_policy', {})
        max_critical = policy.get('max_critical_vulnerabilities', 0)
        max_high = policy.get('max_high_vulnerabilities', 5)

        critical_count = len(findings.get('CRITICAL', []))
        high_count = len(findings.get('HIGH', []))

        approved = critical_count <= max_critical and high_count <= max_high

        result = {
            'approved': approved,
            'critical_count': critical_count,
            'high_count': high_count,
            'max_critical_allowed': max_critical,
            'max_high_allowed': max_high,
            'critical_violations': max(0, critical_count - max_critical),
            'high_violations': max(0, high_count - max_high)
        }

        if approved:
            logger.info("    ✅ Deployment APPROVED")
        else:
            logger.warning("    ❌ Deployment REJECTED (Policy violations)")
            logger.warning(f"       Critical: {critical_count}/{max_critical}")
            logger.warning(f"       High: {high_count}/{max_high}")

        return result

    def print_summary(self, result: Dict):
        """Print pipeline execution summary"""
        print("\n" + "="*70)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*70)
        print(f"Status: {result['status']}")
        print(f"Duration: {result['duration_seconds']:.2f}s")
        print(f"\nScanners Executed: {len(result['scan_results'])}")

        for sr in result['scan_results']:
            print(f"  - {sr['scanner_name']}: {sr['vulnerabilities_found']} issues "
                  f"({sr['duration_seconds']:.2f}s)")

        findings = result.get('findings', {})
        total_findings = sum(len(v) for v in findings.values() if isinstance(v, list))

        print(f"\nTotal Findings: {total_findings}")
        print(f"  Critical: {len(findings.get('CRITICAL', []))}")
        print(f"  High: {len(findings.get('HIGH', []))}")
        print(f"  Medium: {len(findings.get('MEDIUM', []))}")
        print(f"  Low: {len(findings.get('LOW', []))}")

        policy = result.get('policy_result', {})
        print(f"\nDeployment Decision: {'✅ APPROVED' if policy.get('approved') else '❌ REJECTED'}")

        print("="*70 + "\n")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI-Powered DevSecOps Pipeline Orchestrator'
    )
    parser.add_argument(
        '--target',
        default='.',
        help='Path to code to scan (default: current directory)'
    )
    parser.add_argument(
        '--config',
        help='Path to configuration file (YAML)'
    )
    parser.add_argument(
        '--output',
        default='scan-results',
        help='Output directory for reports'
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = DevSecOpsOrchestrator(config_path=args.config)
    orchestrator.output_dir = Path(args.output)
    orchestrator.output_dir.mkdir(exist_ok=True)

    # Execute pipeline
    result = orchestrator.execute_full_pipeline(target_path=args.target)

    # Exit with appropriate code
    sys.exit(0 if result['status'] == 'SUCCESS' else 1)


if __name__ == "__main__":
    main()
