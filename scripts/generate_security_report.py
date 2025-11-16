#!/usr/bin/env python3
"""
Generate HTML security assessment report from findings
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Assessment Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}

        .subtitle {{
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}

        .stat-card {{
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .stat-card.critical {{
            background: #fee;
            border-left: 4px solid #e74c3c;
        }}

        .stat-card.high {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
        }}

        .stat-card.medium {{
            background: #fff9e6;
            border-left: 4px solid #ffc107;
        }}

        .stat-card.low {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
        }}

        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}

        .stat-label {{
            color: #666;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 1px;
        }}

        .section {{
            margin: 40px 0;
        }}

        .section-title {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }}

        .vulnerability {{
            background: #fafafa;
            padding: 20px;
            margin: 15px 0;
            border-radius: 6px;
            border-left: 4px solid #bdc3c7;
        }}

        .vulnerability.critical {{
            border-left-color: #e74c3c;
            background: #fee;
        }}

        .vulnerability.high {{
            border-left-color: #ff9800;
            background: #fff3e0;
        }}

        .vulnerability.medium {{
            border-left-color: #ffc107;
            background: #fff9e6;
        }}

        .vuln-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .vuln-type {{
            font-weight: bold;
            font-size: 1.2em;
            color: #2c3e50;
        }}

        .vuln-severity {{
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.85em;
        }}

        .severity-critical {{ background: #e74c3c; }}
        .severity-high {{ background: #ff9800; }}
        .severity-medium {{ background: #ffc107; }}
        .severity-low {{ background: #4caf50; }}

        .vuln-details {{
            color: #555;
            margin: 10px 0;
        }}

        .vuln-file {{
            font-family: 'Courier New', monospace;
            background: #f0f0f0;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 10px 0;
            color: #333;
        }}

        .confidence-bar {{
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }}

        .confidence-fill {{
            height: 100%;
            background: #3498db;
            transition: width 0.3s;
        }}

        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #777;
        }}

        .no-findings {{
            padding: 40px;
            text-align: center;
            color: #4caf50;
            background: #e8f5e9;
            border-radius: 8px;
            font-size: 1.2em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Security Assessment Report</h1>
        <div class="subtitle">AI-Powered DevSecOps Pipeline | Generated {date}</div>

        <div class="summary">
            <div class="stat-card critical">
                <div class="stat-label">Critical</div>
                <div class="stat-number">{critical_count}</div>
            </div>
            <div class="stat-card high">
                <div class="stat-label">High</div>
                <div class="stat-number">{high_count}</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-label">Medium</div>
                <div class="stat-number">{medium_count}</div>
            </div>
            <div class="stat-card low">
                <div class="stat-label">Low</div>
                <div class="stat-number">{low_count}</div>
            </div>
        </div>

        {sections}

        <div class="footer">
            <p>Generated by AI-Powered DevSecOps Pipeline</p>
            <p>False positives filtered: {fp_filtered} | Total raw alerts: {total_raw}</p>
        </div>
    </div>
</body>
</html>
"""


def generate_html_report(findings: dict, output_file: Path):
    """Generate HTML report from findings"""

    # Count findings
    critical = findings.get('CRITICAL', [])
    high = findings.get('HIGH', [])
    medium = findings.get('MEDIUM', [])
    low = findings.get('LOW', [])

    total = len(critical) + len(high) + len(medium) + len(low)

    # Generate sections
    sections_html = []

    if total == 0:
        sections_html.append('<div class="no-findings">✅ No security vulnerabilities detected!</div>')
    else:
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            vulns = findings.get(severity, [])
            if vulns:
                section_html = f'<div class="section"><h2 class="section-title">{severity} Severity ({len(vulns)})</h2>'

                for vuln in vulns[:50]:  # Limit to 50 per severity
                    vuln_html = f"""
                    <div class="vulnerability {severity.lower()}">
                        <div class="vuln-header">
                            <div class="vuln-type">{vuln.get('type', 'UNKNOWN')}</div>
                            <div class="vuln-severity severity-{severity.lower()}">{severity}</div>
                        </div>
                        <div class="vuln-details">{vuln.get('message', 'No description available')}</div>
                        <div class="vuln-file">📄 {vuln.get('file', 'N/A')}:{vuln.get('line', 0)}</div>
                        <div>Confidence: {vuln.get('confidence', 0.5):.0%}</div>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {vuln.get('confidence', 0.5) * 100}%"></div>
                        </div>
                    </div>
                    """
                    section_html += vuln_html

                section_html += '</div>'
                sections_html.append(section_html)

    # Fill template
    html = HTML_TEMPLATE.format(
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        critical_count=len(critical),
        high_count=len(high),
        medium_count=len(medium),
        low_count=len(low),
        sections='\n'.join(sections_html),
        fp_filtered=findings.get('false_positives_filtered', 0),
        total_raw=findings.get('total_raw_alerts', total)
    )

    # Write to file
    with open(output_file, 'w') as f:
        f.write(html)

    logger.info(f"HTML report generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate security assessment report')
    parser.add_argument('--findings', type=Path, required=True, help='Input findings JSON')
    parser.add_argument('--format', choices=['html', 'json'], default='html', help='Output format')
    parser.add_argument('--output', type=Path, required=True, help='Output file')

    args = parser.parse_args()

    # Load findings
    try:
        with open(args.findings) as f:
            findings = json.load(f)
    except FileNotFoundError:
        logger.error(f"Findings file not found: {args.findings}")
        # Create empty findings
        findings = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': [],
            'INFO': [],
            'false_positives_filtered': 0,
            'total_raw_alerts': 0
        }

    # Generate report
    if args.format == 'html':
        generate_html_report(findings, args.output)
    else:
        # JSON format
        with open(args.output, 'w') as f:
            json.dump(findings, f, indent=2)
        logger.info(f"JSON report generated: {args.output}")


if __name__ == '__main__':
    main()
