#!/bin/bash
echo "🚀 Starting Hack for Social Good Backend..."
cd "$(dirname "$0")"

# Load environment variables
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | xargs) 2>/dev/null || true
fi

# Start server with uv if available, otherwise use venv
if command -v uv &> /dev/null; then
    echo "📡 Starting server with uv on http://localhost:8000"
    uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    echo "📡 Starting server with venv on http://localhost:8000"
    source .venv/bin/activate
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi
