# Vulnerable Flask Application

**⚠️ WARNING: FOR SECURITY TESTING ONLY ⚠️**

This application is **intentionally vulnerable** and should **NEVER** be deployed to production or exposed to the internet.

## Purpose

This application is designed to test the AI-Powered DevSecOps Pipeline's ability to detect common web application vulnerabilities.

## Vulnerabilities Included

1. **SQL Injection (CWE-89)** - `/search` endpoint
2. **Cross-Site Scripting (CWE-79)** - `/greet` endpoint
3. **Hardcoded Credentials (CWE-798)** - Throughout the code
4. **Path Traversal (CWE-22)** - `/file` endpoint
5. **Command Injection (CWE-78)** - `/ping` endpoint
6. **Insecure Deserialization (CWE-502)** - `/deserialize` endpoint
7. **Weak Cryptography (CWE-327)** - `/hash` endpoint
8. **Broken Access Control (CWE-285)** - `/admin` endpoint
9. **Open Redirect (CWE-601)** - `/redirect` endpoint
10. **Debug Mode Enabled** - Flask debug mode in production

## Running Locally

```bash
cd sample-apps/vulnerable-flask-app
pip install -r requirements.txt
python app.py
```

Access at: http://localhost:5000

## Expected Scanner Results

When scanned with the DevSecOps pipeline, this application should trigger:

- **Bandit**: 8-12 issues (hardcoded credentials, SQL injection patterns, etc.)
- **Semgrep**: 5-10 issues (security anti-patterns)
- **Safety**: 3-5 dependency vulnerabilities
- **CodeBERT ML Model**: Detection of semantic vulnerabilities

## Testing the Pipeline

```bash
# From repository root
python scripts/orchestrate_devsecops.py \
  --target sample-apps/vulnerable-flask-app \
  --output test-results
```

## License

Educational Use Only - Not for production deployment
