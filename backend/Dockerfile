# Use Python 3.13 slim image for smaller size
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv package manager
# Using the official installation method from astral.sh
RUN pip install --no-cache-dir uv

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml ./

# Install dependencies using uv
# --system flag installs packages globally (no virtual environment needed in container)
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (Cloud Run will set this via $PORT environment variable)
# Default to 8080 if PORT is not set
ENV PORT=8080

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health').read()"

# Start the application
# Use $PORT environment variable for Cloud Run compatibility
# --host 0.0.0.0 allows external access
# --workers 1 is sufficient for Cloud Run (Cloud Run handles scaling)
CMD uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
