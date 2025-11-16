#!/usr/bin/env python3
"""
Train Correlation Model Example
================================

This example demonstrates how to train the alert correlation engine
on your own labeled data to improve false positive detection.
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from ml_models.alert_correlation_engine import AlertCorrelationEngine


def create_sample_training_data():
    """Create sample training data with analyst feedback"""
    # This would typically come from your security team's reviews
    training_data = [
        # True positives
        {
            'type': 'SQL_INJECTION',
            'severity': 'CRITICAL',
            'file': 'routes.py',
            'line': 42,
            'confidence': 0.95,
            'reported_by': ['Bandit', 'Semgrep'],
            'asset_criticality': 5,
            'is_false_positive': 0  # LABEL: True positive
        },
        {
            'type': 'HARDCODED_CREDENTIALS',
            'severity': 'HIGH',
            'file': 'config.py',
            'line': 10,
            'confidence': 0.90,
            'reported_by': ['Bandit'],
            'asset_criticality': 4,
            'is_false_positive': 0  # LABEL: True positive
        },

        # False positives
        {
            'type': 'WEAK_CRYPTOGRAPHY',
            'severity': 'MEDIUM',
            'file': 'test_utils.py',  # Test file
            'line': 15,
            'confidence': 0.65,
            'reported_by': ['Bandit'],
            'asset_criticality': 1,  # Low criticality (test code)
            'is_false_positive': 1  # LABEL: False positive
        },
        {
            'type': 'COMMAND_INJECTION',
            'severity': 'HIGH',
            'file': 'build.py',
            'line': 100,
            'confidence': 0.60,
            'reported_by': ['Semgrep'],
            'asset_criticality': 2,
            'is_false_positive': 1  # LABEL: False positive (build script)
        },

        # Add more labeled examples...
        # In practice, you'd have 100s-1000s of labeled alerts
    ]

    return training_data


def train_model():
    """Train the correlation model with labeled data"""
    print("=" * 70)
    print("TRAINING CORRELATION MODEL")
    print("=" * 70)
    print()

    # Step 1: Load or create training data
    print("1. Loading training data...")
    training_data = create_sample_training_data()
    print(f"   Loaded {len(training_data)} labeled alerts")

    # Count true vs false positives
    true_positives = sum(1 for alert in training_data if not alert['is_false_positive'])
    false_positives = sum(1 for alert in training_data if alert['is_false_positive'])
    print(f"   True positives: {true_positives}")
    print(f"   False positives: {false_positives}")

    # Step 2: Initialize correlation engine
    print("\n2. Initializing correlation engine...")
    engine = AlertCorrelationEngine()

    # Step 3: Train on labeled data
    print("\n3. Training model...")
    engine.train_on_feedback(
        labeled_alerts=training_data,
        save_model_path='models/trained_correlation_model.pkl'
    )
    print("   ✓ Model trained successfully!")

    # Step 4: Test the trained model
    print("\n4. Testing trained model...")

    # Create test alerts (without labels)
    test_alerts = [
        {
            'type': 'SQL_INJECTION',
            'severity': 'CRITICAL',
            'file': 'api.py',
            'line': 25,
            'confidence': 0.92,
            'reported_by': ['Bandit', 'Semgrep', 'CodeBERT'],
            'asset_criticality': 5,
        },
        {
            'type': 'WEAK_CRYPTOGRAPHY',
            'severity': 'LOW',
            'file': 'test_crypto.py',  # Likely false positive
            'line': 8,
            'confidence': 0.55,
            'reported_by': ['Bandit'],
            'asset_criticality': 1,
        }
    ]

    # Run correlation
    results = engine.correlate_and_prioritize(test_alerts)

    # Show predictions
    print("\n   Predictions:")
    for alert in test_alerts:
        # Find corresponding result
        for severity, alerts in results.items():
            for result_alert in alerts:
                if result_alert.get('type') == alert['type']:
                    fp_likelihood = result_alert.get('false_positive_likelihood', 0)
                    print(f"   - {alert['type']} in {alert['file']}")
                    print(f"     FP Likelihood: {fp_likelihood:.2%}")
                    if fp_likelihood > 0.8:
                        print(f"     → Would be filtered as FALSE POSITIVE")
                    else:
                        print(f"     → Kept as TRUE POSITIVE")
                    print()

    # Step 5: Save training data for future reference
    print("5. Saving training data...")
    training_file = Path('models/training_data.json')
    training_file.parent.mkdir(exist_ok=True)
    with open(training_file, 'w') as f:
        json.dump(training_data, f, indent=2)
    print(f"   Saved to {training_file}")

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print()
    print("To use the trained model:")
    print("1. The model is automatically loaded from models/trained_correlation_model.pkl")
    print("2. Run scans as usual - the trained model will be used for correlation")
    print("3. Continue adding feedback to improve accuracy over time")
    print()


def continuous_learning_example():
    """Example of continuous learning workflow"""
    print("\n" + "=" * 70)
    print("CONTINUOUS LEARNING WORKFLOW")
    print("=" * 70)
    print()

    print("Recommended workflow for continuous improvement:")
    print()
    print("1. Run initial scans with default model")
    print("2. Security analysts review findings")
    print("3. Mark false positives in results")
    print("4. Export labeled data:")
    print("   python scripts/export_labels.py --output labels.json")
    print()
    print("5. Retrain model monthly:")
    print("   python examples/advanced/train_correlation_model.py")
    print()
    print("6. Evaluate improvement:")
    print("   - Track false positive rate over time")
    print("   - Monitor analyst time saved")
    print("   - Measure accuracy on validation set")
    print()


if __name__ == "__main__":
    train_model()
    continuous_learning_example()
