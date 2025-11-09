#!/bin/bash
# 🚀 Quick Setup for Hack for Social Good Backend
# Auto-generates service account and environment files

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Quick Backend Setup${NC}"
echo "=========================="

# Get script directory and check if we're in the right place
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -f "main.py" ]]; then
    echo -e "${RED}❌ Please run this script from the backend directory${NC}"
    exit 1
fi

echo -e "${BLUE}📍 Current directory: $(pwd)${NC}"

# 1. Generate mock service account if it doesn't exist
if [[ ! -f "service-account.json" ]]; then
    echo -e "${BLUE}� Generating mock service account...${NC}"
    cat > service-account.json << 'EOF'
{
  "type": "service_account",
  "project_id": "hack-for-social-good-dev",
  "private_key_id": "dev-key-123",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMOCK_KEY_FOR_DEVELOPMENT\n-----END PRIVATE KEY-----\n",
  "client_email": "dev@hack-for-social-good-dev.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dev%40hack-for-social-good-dev.iam.gserviceaccount.com"
}
EOF
    echo -e "${GREEN}✅ Mock service account created${NC}"
else
    echo -e "${GREEN}✅ Service account file already exists${NC}"
fi

# 2. Generate .env file if it doesn't exist  
if [[ ! -f ".env" ]]; then
    echo -e "${BLUE}⚙️  Generating .env file...${NC}"
    
    # Prompt for Gemini API key
    echo -e "${YELLOW}Enter your Gemini API key (or press Enter to skip):${NC}"
    read -r gemini_key
    
    cat > .env << EOF
# 🔐 Hack for Social Good Backend Configuration
# Generated on $(date)

# =============================================================================
# AI Configuration
# =============================================================================
GEMINI_API_KEY=${gemini_key:-""}

# =============================================================================
# Google Cloud Storage Configuration
# =============================================================================
GOOGLE_APPLICATION_CREDENTIALS=${SCRIPT_DIR}/service-account.json
GCS_BUCKET_NAME=hack-for-social-good-uploads

# =============================================================================
# API Configuration
# =============================================================================
API_TITLE="PDF Analysis API for Social Good"
API_VERSION="1.0.0"
MAX_FILE_SIZE=10485760
ALLOWED_ORIGINS=["*"]

# =============================================================================
# Development Settings
# =============================================================================
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
EOF
    echo -e "${GREEN}✅ Environment file created${NC}"
else
    echo -e "${GREEN}✅ Environment file already exists${NC}"
fi

# 3. Install dependencies using uv
echo -e "${BLUE}� Installing dependencies with uv...${NC}"
if command -v uv &> /dev/null; then
    uv sync
    echo -e "${GREEN}✅ Dependencies installed with uv${NC}"
else
    echo -e "${YELLOW}⚠️  uv not found, falling back to pip...${NC}"
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install --upgrade pip
    pip install fastapi uvicorn[standard] google-generativeai google-cloud-storage PyPDF2 python-multipart python-dotenv requests
    echo -e "${GREEN}✅ Dependencies installed with pip${NC}"
fi

# 4. Create start script
if [[ ! -f "start.sh" ]]; then
    echo -e "${BLUE}� Creating start script...${NC}"
    cat > start.sh << 'EOF'
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
EOF
    chmod +x start.sh
    echo -e "${GREEN}✅ Start script created${NC}"
fi

# 5. Test setup
echo -e "${BLUE}🧪 Testing setup...${NC}"
if command -v uv &> /dev/null; then
    if uv run python -c "import fastapi, uvicorn; print('Core modules OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ Installation test passed${NC}"
    else
        echo -e "${RED}❌ Installation test failed${NC}"
    fi
else
    source .venv/bin/activate
    if python -c "import fastapi, uvicorn; print('Core modules OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ Installation test passed${NC}"
    else
        echo -e "${RED}❌ Installation test failed${NC}"
    fi
fi

echo
echo -e "${GREEN}🎉 Quick setup complete!${NC}"
echo
echo -e "${BLUE}📋 Next steps:${NC}"
echo -e "${BLUE}1. Start the server:${NC} ./start.sh"
echo -e "${BLUE}2. API docs:${NC} http://localhost:8000/docs"
echo -e "${BLUE}3. Health check:${NC} http://localhost:8000/health"
echo
if [[ -z "$gemini_key" ]]; then
    echo -e "${YELLOW}⚠️  Add your GEMINI_API_KEY to .env for AI features${NC}"
    echo -e "${YELLOW}   Get it at: https://aistudio.google.com/${NC}"
fi
echo -e "${YELLOW}⚠️  Using mock GCS credentials for development${NC}"