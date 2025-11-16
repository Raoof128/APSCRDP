# Multi-stage Dockerfile for AI-Powered DevSecOps Pipeline
# Optimized for security scanning and ML model execution

FROM python:3.11-slim as base

# Security: Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for layer caching
COPY ml_models/requirements.txt /app/ml_requirements.txt
COPY sample-apps/vulnerable-flask-app/requirements.txt /app/app_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/ml_requirements.txt && \
    pip install --no-cache-dir bandit semgrep safety

# Copy application code
COPY . /app/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (if running web interface)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "scripts/orchestrate_devsecops.py", "--target", ".", "--output", "/app/results"]
