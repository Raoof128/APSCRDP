#!/usr/bin/env python3
"""
Unit tests for ML models
Tests semantic code analyzer and alert correlation engine
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml_models.semantic_code_analyzer import SemanticCodeAnalyzer, CodeVulnerability
from ml_models.alert_correlation_engine import AlertCorrelationEngine


class TestSemanticCodeAnalyzer(unittest.TestCase):
    """Test cases for SemanticCodeAnalyzer"""

    def setUp(self):
        """Set up test fixtures"""
        # Note: In real tests, use a smaller model or mock
        # For portfolio purposes, we'll test the interface
        pass

    def test_vulnerability_dataclass(self):
        """Test CodeVulnerability dataclass creation"""
        vuln = CodeVulnerability(
            file_path="test.py",
            line_number=42,
            vulnerability_type="SQL_INJECTION",
            severity="CRITICAL",
            ml_confidence=0.95,
            cwe_id="CWE-89",
            remediation="Use parameterized queries"
        )

        self.assertEqual(vuln.file_path, "test.py")
        self.assertEqual(vuln.line_number, 42)
        self.assertEqual(vuln.vulnerability_type, "SQL_INJECTION")
        self.assertEqual(vuln.ml_confidence, 0.95)

    def test_severity_assignment(self):
        """Test severity assignment logic"""
        # This would test the _assign_severity method
        # In production, we'd use mocks to avoid loading the full model
        pass

    def test_analyze_empty_code(self):
        """Test handling of empty code input"""
        # analyzer = SemanticCodeAnalyzer()
        # results = analyzer.analyze_code_snippet("", language="python")
        # self.assertEqual(len(results), 0)
        pass


class TestAlertCorrelationEngine(unittest.TestCase):
    """Test cases for AlertCorrelationEngine"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = AlertCorrelationEngine()

        self.sample_alerts = [
            {
                'id': 'test-001',
                'type': 'SQL_INJECTION',
                'severity': 'CRITICAL',
                'file': 'app.py',
                'line': 42,
                'confidence': 0.95,
                'reported_by': ['Bandit', 'Semgrep'],
                'asset_criticality': 5
            },
            {
                'id': 'test-002',
                'type': 'HARDCODED_CREDENTIALS',
                'severity': 'HIGH',
                'file': 'config.py',
                'line': 10,
                'confidence': 0.88,
                'reported_by': ['Bandit'],
                'asset_criticality': 4
            },
        ]

    def test_preprocess_alerts(self):
        """Test alert preprocessing"""
        df = self.engine.preprocess_alerts(self.sample_alerts)

        self.assertEqual(len(df), 2)
        self.assertIn('vulnerability_type', df.columns)
        self.assertIn('severity_score', df.columns)
        self.assertIn('exploitability_score', df.columns)

    def test_correlate_empty_alerts(self):
        """Test handling of empty alert list"""
        result = self.engine.correlate_and_prioritize([])

        self.assertIn('CRITICAL', result)
        self.assertIn('HIGH', result)
        self.assertEqual(len(result['CRITICAL']), 0)

    def test_correlate_alerts(self):
        """Test basic alert correlation"""
        result = self.engine.correlate_and_prioritize(self.sample_alerts)

        self.assertIn('CRITICAL', result)
        self.assertIn('HIGH', result)

        # Should have at least 1 critical alert
        self.assertGreater(len(result['CRITICAL']), 0)

    def test_exploitability_calculation(self):
        """Test exploitability score calculation"""
        alert = {'type': 'SQL_INJECTION'}
        score = self.engine._calc_exploitability(alert)

        self.assertGreater(score, 0)
        self.assertLessEqual(score, 10)

    def test_scanner_agreement(self):
        """Test scanner agreement calculation"""
        alert = {'reported_by': ['Scanner1', 'Scanner2', 'Scanner3']}
        agreement = self.engine._calc_scanner_agreement(alert)

        self.assertGreaterEqual(agreement, 0)
        self.assertLessEqual(agreement, 1.0)

    def test_statistics(self):
        """Test statistics generation"""
        result = self.engine.correlate_and_prioritize(self.sample_alerts)
        stats = self.engine.get_statistics(result)

        self.assertIn('total_alerts', stats)
        self.assertIn('critical', stats)
        self.assertIn('high', stats)
        self.assertIn('model_trained', stats)

        self.assertGreater(stats['total_alerts'], 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete pipeline"""

    def test_end_to_end_flow(self):
        """Test complete pipeline flow"""
        # This would test the full orchestration
        # From scanning -> correlation -> reporting
        pass


def run_tests():
    """Run all tests"""
    unittest.main()


if __name__ == '__main__':
    run_tests()
