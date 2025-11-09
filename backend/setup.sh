#!/bin/bash

# 🚀 Auto Setup Script for Hack for Social Good Backend
# This script generates service account credentials and environment files

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR"

echo -e "${BLUE}🚀 Hack for Social Good Backend Auto Setup${NC}"
echo -e "${BLUE}=================================================${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Generate mock service account file (for development)
generate_service_account() {
    local service_account_file="$BACKEND_DIR/service-account.json"
    
    print_info "Generating mock service account file..."
    
    # Check if service account already exists
    if [[ -f "$service_account_file" ]]; then
        print_warning "Service account file already exists at: $service_account_file"
        read -p "Do you want to overwrite it? (y/N): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Keeping existing service account file"
            return 0
        fi
    fi
    
    # Generate a mock service account for development
    cat > "$service_account_file" << 'EOF'
{
  "type": "service_account",
  "project_id": "hack-for-social-good-dev",
  "private_key_id": "dev-key-id-123456789",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMOCK_PRIVATE_KEY_FOR_DEVELOPMENT_ONLY\n-----END PRIVATE KEY-----\n",
  "client_email": "dev-service@hack-for-social-good-dev.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dev-service%40hack-for-social-good-dev.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
EOF
    
    print_status "Mock service account file generated: $service_account_file"
    print_warning "This is a mock file for development. Replace with real credentials for production!"
}

# Generate .env file
generate_env_file() {
    local env_file="$BACKEND_DIR/.env"
    
    print_info "Generating environment file..."
    
    # Check if .env already exists
    if [[ -f "$env_file" ]]; then
        print_warning "Environment file already exists at: $env_file"
        read -p "Do you want to overwrite it? (y/N): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Keeping existing environment file"
            return 0
        fi
    fi
    
    # Prompt for Gemini API key
    echo
    print_info "Setting up environment variables..."
    
    # Get Gemini API key
    read -p "Enter your Gemini API key (or press Enter to use mock analysis): " gemini_key
    
    # Get GCS bucket name
    read -p "Enter GCS bucket name (default: hack-for-social-good-uploads): " bucket_name
    bucket_name=${bucket_name:-hack-for-social-good-uploads}
    
    # Generate .env file
    cat > "$env_file" << EOF
# 🔐 Environment Configuration for Hack for Social Good Backend
# Generated on $(date)

# =============================================================================
# AI Configuration
# =============================================================================
# Gemini API Key (get from: https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=${gemini_key:-""}

# =============================================================================
# Google Cloud Storage Configuration
# =============================================================================
# Path to service account JSON file
GOOGLE_APPLICATION_CREDENTIALS=${BACKEND_DIR}/service-account.json

# GCS Bucket name for file uploads
GCS_BUCKET_NAME=${bucket_name}

# =============================================================================
# API Configuration
# =============================================================================
# FastAPI settings
API_TITLE="PDF Analysis API for Social Good"
API_VERSION="1.0.0"

# File upload limits (in bytes)
MAX_FILE_SIZE=10485760  # 10MB

# CORS settings (adjust for production)
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]

# =============================================================================
# Development Settings
# =============================================================================
# Environment mode
ENVIRONMENT=development

# Debug mode
DEBUG=true

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
EOF

    print_status "Environment file generated: $env_file"
}

# Install dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Please install it first:"
        print_info "curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    cd "$BACKEND_DIR"
    
    # Sync dependencies
    print_info "Syncing dependencies with uv..."
    uv sync
    
    print_status "Dependencies installed successfully!"
}

# Create startup script
create_startup_script() {
    local startup_script="$BACKEND_DIR/start_server.sh"
    
    print_info "Creating startup script..."
    
    cat > "$startup_script" << 'EOF'
#!/bin/bash

# 🚀 Backend Server Startup Script
# This script starts the FastAPI server with proper environment configuration

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting Hack for Social Good Backend Server${NC}"
echo -e "${BLUE}=============================================${NC}"

# Check if .env exists
if [[ ! -f ".env" ]]; then
    echo -e "${RED}❌ .env file not found. Run ./setup.sh first${NC}"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Start server with uv
echo -e "${GREEN}✅ Starting server on http://0.0.0.0:8000${NC}"
echo -e "${BLUE}   API Documentation: http://localhost:8000/docs${NC}"
echo -e "${BLUE}   Press Ctrl+C to stop${NC}"
echo

uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOF

    chmod +x "$startup_script"
    print_status "Startup script created: $startup_script"
}

# Create test script
create_test_script() {
    local test_script="$BACKEND_DIR/test_setup.py"
    
    print_info "Creating test script..."
    
    cat > "$test_script" << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify backend setup and functionality.
"""

import os
import sys
import requests
import time
import subprocess
from pathlib import Path

def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment configuration...")
    
    # Check .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Check service account file
    service_account = Path("service-account.json")
    if not service_account.exists():
        print("❌ service-account.json not found")
        return False
    
    print("✅ Environment files found")
    return True

def test_server_startup():
    """Test if server can start."""
    print("\n🚀 Testing server startup...")
    
    try:
        # Start server in background
        process = subprocess.Popen(
            ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test health endpoint
        response = requests.get("http://localhost:8001/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ Server started successfully")
            print(f"   Health check: {response.json()}")
            result = True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            result = False
            
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        result = False
    finally:
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
    
    return result

def test_pdf_analysis():
    """Test PDF analysis functionality."""
    print("\n📄 Testing PDF analysis...")
    
    # Check if test PDF exists
    test_pdf = Path("pdf/Young-AK2960-2024-10-24.pdf")
    if not test_pdf.exists():
        print("⚠️  Test PDF not found, skipping analysis test")
        return True
    
    try:
        # Test text extraction
        with open(test_pdf, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = requests.post("http://localhost:8001/pdf/extract-text", files=files, timeout=30)
        
        if response.status_code == 200:
            print("✅ PDF analysis working")
            return True
        else:
            print(f"❌ PDF analysis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ PDF analysis error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Backend Setup Test Suite")
    print("=" * 40)
    
    tests = [
        ("Environment Configuration", check_environment),
        ("Server Startup", test_server_startup),
        ("PDF Analysis", test_pdf_analysis),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:<25}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

    chmod +x "$test_script"
    print_status "Test script created: $test_script"
}

# Main setup function
main() {
    echo
    print_info "This script will set up the backend environment for development"
    print_info "Location: $BACKEND_DIR"
    echo
    
    # Confirm setup
    read -p "Continue with setup? (y/N): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Setup cancelled"
        exit 0
    fi
    
    echo
    
    # Run setup steps
    generate_service_account
    generate_env_file
    install_dependencies
    create_startup_script
    create_test_script
    
    echo
    print_status "🎉 Backend setup complete!"
    echo
    print_info "Next steps:"
    print_info "1. Start the server: ./start_server.sh"
    print_info "2. Test the setup: python test_setup.py"
    print_info "3. View API docs: http://localhost:8000/docs"
    echo
    print_warning "Remember to replace the mock service account with real credentials for production!"
    echo
}

# Run main function
main "$@"