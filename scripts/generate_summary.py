#!/usr/bin/env python3
"""
Generate GitHub summary from findings JSON
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("### ⚠️ Security Assessment")
        print("No findings file provided")
        return

    findings_file = Path(sys.argv[1])

    if not findings_file.exists():
        print("### ⚠️ Security Assessment")
        print("Findings file not found")
        return

    try:
        with open(findings_file) as f:
            findings = json.load(f)

        critical = len(findings.get('CRITICAL', []))
        high = len(findings.get('HIGH', []))
        medium = len(findings.get('MEDIUM', []))
        low = len(findings.get('LOW', []))
        total = critical + high + medium + low

        fp_filtered = findings.get('false_positives_filtered', 0)
        total_raw = findings.get('total_raw_alerts', total)

        # Generate markdown summary
        print("### 🛡️ Security Assessment Summary")
        print()
        print("| Severity | Count |")
        print("|----------|-------|")
        print(f"| 🔴 **Critical** | {critical} |")
        print(f"| 🟠 **High** | {high} |")
        print(f"| 🟡 **Medium** | {medium} |")
        print(f"| 🟢 **Low** | {low} |")
        print()
        print(f"**Total Findings:** {total}")
        print(f"**Raw Alerts:** {total_raw}")
        print(f"**False Positives Filtered:** {fp_filtered} ({fp_filtered/max(total_raw,1)*100:.1f}%)")
        print()

        if critical > 0:
            print("⚠️ **Action Required:** Critical vulnerabilities detected!")
        elif high > 0:
            print("⚠️ **Attention:** High severity vulnerabilities detected")
        elif total == 0:
            print("✅ **No vulnerabilities detected** - Deployment approved")
        else:
            print("✅ **Low risk** - Review medium/low findings")

        # List critical/high findings
        if critical > 0 or high > 0:
            print()
            print("#### Top Priority Issues")
            print()

            for vuln in findings.get('CRITICAL', [])[:5]:
                print(f"- 🔴 **{vuln.get('type', 'Unknown')}** in `{vuln.get('file', 'N/A')}:{vuln.get('line', 0)}`")

            for vuln in findings.get('HIGH', [])[:5]:
                print(f"- 🟠 **{vuln.get('type', 'Unknown')}** in `{vuln.get('file', 'N/A')}:{vuln.get('line', 0)}`")

    except Exception as e:
        print("### ⚠️ Security Assessment Error")
        print(f"Failed to generate summary: {e}")


if __name__ == '__main__':
    main()
