# Backend API

A FastAPI-based backend server with PDF processing and Google Gemini AI integration for converting PDFs to markdown.

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** ([Download Python](https://python.org/downloads/))
- **Git** ([Download Git](https://git-scm.com/downloads/))
- **Google Gemini API Key** ([Get API Key](https://aistudio.google.com/))

### 📦 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/hack-four-social-impact/hack-for-social-impact.git
   cd hack-for-social-impact/backend
   ```

2. **Create and activate virtual environment**

   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate it
   # On macOS/Linux:
   source .venv/bin/activate

   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   # Install all required packages
   pip install fastapi uvicorn[standard] google-generativeai PyPDF2 python-multipart python-dotenv requests

   # Or use the project configuration:
   pip install -e .
   ```

4. **Configure environment variables**

   ```bash
   # Copy the example file (if it exists)
   cp .env.example .env  # Skip if file doesn't exist

   # Create .env file with your API key
   echo "GEMINI_API_KEY=your_actual_gemini_api_key_here" > .env
   echo "HOST=0.0.0.0" >> .env
   echo "PORT=8000" >> .env
   echo "DEBUG=True" >> .env
   ```

5. **Get your Gemini API Key**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key and replace `your_actual_gemini_api_key_here` in your `.env` file

## 🏃‍♂️ Running the Server

### Option 1: Quick Start (Development)

```bash
# Make sure you're in the backend directory and virtual environment is active
cd main/backend
source .venv/bin/activate  # On macOS/Linux
uvicorn main:app --reload
```

### Option 2: Custom Configuration

```bash
# Run on specific host and port
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Run on all interfaces (for network access)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Production Mode

```bash
# For production deployment
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### ✅ Verify It's Working

Once the server starts, you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test the API:**

- Open your browser and go to: http://localhost:8000/docs
- You should see the interactive API documentation (Swagger UI)

## 🌐 API Access

| Resource           | URL                                  | Description                   |
| ------------------ | ------------------------------------ | ----------------------------- |
| **API Base**       | `http://localhost:8000`              | Main API endpoint             |
| **Swagger UI**     | `http://localhost:8000/docs`         | Interactive API documentation |
| **ReDoc**          | `http://localhost:8000/redoc`        | Alternative API documentation |
| **OpenAPI Schema** | `http://localhost:8000/openapi.json` | API schema in JSON format     |
| **Health Check**   | `http://localhost:8000/health`       | Server health status          |

## 📋 API Endpoints

### 🏥 Health & Status

| Method | Endpoint  | Description                                   |
| ------ | --------- | --------------------------------------------- |
| `GET`  | `/`       | API information and welcome message           |
| `GET`  | `/health` | Health check + Gemini AI configuration status |

### 📄 PDF Processing

| Method | Endpoint                  | Description                                        | Parameters                                                 |
| ------ | ------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| `POST` | `/pdf/process`            | Upload PDF + AI markdown conversion (general)      | `file` (PDF), `prompt` (optional), `max_tokens` (optional) |
| `POST` | `/pdf/parole-summary`     | Generate parole hearing summary with citations     | `file` (PDF)                                               |
| `POST` | `/pdf/innocence-analysis` | **NEW** Analyze documents for innocence indicators | `file` (PDF)                                               |
| `POST` | `/pdf/extract-text`       | Extract text from PDF only (no AI processing)      | `file` (PDF)                                               |

#### Detailed Endpoint Information

##### `/pdf/parole-summary` 🎯 **Recommended for Parole Documents**

**Purpose**: Specialized endpoint for generating structured parole hearing summaries with precise line number citations.

**Request**:

```bash
curl -X POST "http://localhost:8000/pdf/parole-summary" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@parole_hearing.pdf"
```

**Response**:

```json
{
  "success": true,
  "filename": "parole_hearing.pdf",
  "file_size": 122133,
  "extracted_text_length": 26175,
  "markdown_summary": "# Parole Hearing Summary\n\n## Offense Context\n- Crime: Second-degree murder - (Line 9)\n...",
  "summary_type": "parole_hearing_summary"
}
```

**Features**:

- ✅ **Page & Line Number Citations**: Every fact includes specific page and line references
- ✅ **Structured Analysis**: Covers offense context, programming, parole factors, contradictions
- ✅ **Direct Quotes**: Includes actual quotes from commissioners and participants
- ✅ **Legal Format**: Professional format suitable for legal review

##### `/pdf/innocence-analysis` 🔍 **NEW: Innocence Detection Analysis**

**Purpose**: Specialized endpoint for analyzing legal documents to detect potential innocence indicators and wrongful conviction evidence.

**Request**:

```bash
curl -X POST "http://localhost:8000/pdf/innocence-analysis" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@legal_document.pdf"
```

**Response**:

```json
{
  "success": true,
  "filename": "legal_document.pdf",
  "file_size": 95432,
  "extracted_text_length": 18750,
  "innocence_analysis": "# Innocence Detection Analysis\n\n## Executive Summary\n...",
  "analysis_type": "innocence_detection",
  "focus_areas": [
    "direct_innocence_claims",
    "procedural_violations",
    "evidence_inconsistencies",
    "witness_issues",
    "new_evidence",
    "wrongful_conviction_patterns"
  ]
}
```

**Features**:

- 🔍 **Wrongful Conviction Analysis**: Detects patterns commonly associated with wrongful convictions
- ⚖️ **Procedural Issue Detection**: Identifies constitutional violations and legal representation problems
- 🧩 **Evidence Inconsistency Analysis**: Highlights contradictions and forensic evidence issues
- 👥 **Witness Reliability Assessment**: Evaluates eyewitness identification and testimony concerns
- 📋 **Structured Legal Analysis**: Professional format suitable for legal review and appeals
- 📍 **Precise Citations**: Page and line number references for all findings

##### `/pdf/process` 🔧 **General PDF Processing**

**Purpose**: Flexible endpoint with custom prompts for various document types.

**Request**:

```bash
curl -X POST "http://localhost:8000/pdf/process" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "prompt=Convert this to markdown with headings and bullet points" \
  -F "max_tokens=2000"
```

**Response**:

```json
{
  "success": true,
  "filename": "document.pdf",
  "file_size": 85641,
  "extracted_text_length": 15420,
  "markdown_summary": "# Document Summary\n\nContent here...",
  "summary_type": "parole_hearing_analysis"
}
```

##### `/pdf/extract-text` 📝 **Text Extraction Only**

**Purpose**: Extract raw text from PDF without AI processing.

**Request**:

```bash
curl -X POST "http://localhost:8000/pdf/extract-text" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Response**:

```json
{
  "success": true,
  "filename": "document.pdf",
  "file_size": 85641,
  "extracted_text": "Raw text content from the PDF..."
}
```

## 🧪 Testing the API

### Method 1: Using the Web Interface (Easiest)

1. Open: http://localhost:8000/docs
2. Click on `/pdf/process` endpoint
3. Click "Try it out"
4. Upload a PDF file
5. Add a custom prompt (optional)
6. Click "Execute"

### Method 2: Using curl (Command Line)

**Generate Parole Hearing Summary (Recommended):**

```bash
curl -X POST "http://localhost:8000/pdf/parole-summary" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/parole_hearing.pdf"
```

**Analyze Documents for Innocence Indicators (NEW):**

```bash
curl -X POST "http://localhost:8000/pdf/innocence-analysis" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/legal_document.pdf"
```

**Process PDF with Custom AI Prompt:**

```bash
curl -X POST "http://localhost:8000/pdf/process" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "prompt=Convert this document to well-formatted markdown with proper headings and structure"
```

**Extract text only:**

```bash
curl -X POST "http://localhost:8000/pdf/extract-text" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

### Method 3: Using Python

```python
import requests

# Generate Parole Hearing Summary (Recommended)
with open('parole_hearing.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/pdf/parole-summary', files=files)
    result = response.json()
    print(result['markdown_summary'])

# Analyze Documents for Innocence Indicators (NEW)
with open('legal_document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/pdf/innocence-analysis', files=files)
    result = response.json()
    print(result['innocence_analysis'])

# Process PDF with Custom Prompt
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {'prompt': 'Convert to markdown format'}
    response = requests.post('http://localhost:8000/pdf/process', files=files, data=data)
    result = response.json()
    print(result['markdown_summary'])

# Extract Text Only
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/pdf/extract-text', files=files)
    result = response.json()
    print(result['extracted_text'])
```

## Development

### Adding New Endpoints

Add new routes to `main.py`:

```python
@app.get("/new-endpoint")
async def new_endpoint():
    return {"message": "This is a new endpoint"}
```

### Environment Variables

Create a `.env` file in the backend directory for environment-specific configurations:

```env
# Required for AI features
GEMINI_API_KEY=your_gemini_api_key_here

# Optional server configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

#### Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your `.env` file

### Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── pyproject.toml       # Project configuration and dependencies
├── README.md           # This file
├── .env               # Environment variables (create from .env.example)
├── .env.example       # Environment variables template
└── api/               # API package
    ├── __init__.py
    ├── core/          # Core configuration
    │   ├── __init__.py
    │   └── config.py  # Application configuration
    ├── routes/        # API route handlers
    │   ├── __init__.py
    │   ├── health.py  # Health check endpoints
    │   └── pdf.py     # PDF processing endpoints
    └── services/      # Business logic services
        ├── __init__.py
        └── pdf_service.py  # PDF and Gemini AI services
```

## 🔧 Troubleshooting

### Common Issues

| Problem                        | Solution                                                                                     |
| ------------------------------ | -------------------------------------------------------------------------------------------- |
| **"Port already in use"**      | Kill existing process: `lsof -ti:8000 \| xargs kill -9` or use different port: `--port 8001` |
| **"Module not found"**         | Activate virtual environment: `source .venv/bin/activate` and reinstall: `pip install -e .`  |
| **"Permission denied"**        | Check file permissions or try without `sudo`                                                 |
| **"GEMINI_API_KEY not found"** | Create `.env` file with your API key (see setup steps above)                                 |
| **"PDF processing failed"**    | Ensure PDF is valid, under 10MB, and contains extractable text                               |

### Environment Issues

**If Gemini AI is not working:**

1. Check your `.env` file exists and contains your API key
2. Verify API key at [Google AI Studio](https://aistudio.google.com/)
3. Check API usage limits and billing
4. Restart the server after updating `.env`

**If dependencies fail to install:**

```bash
# Upgrade pip first
pip install --upgrade pip

# Install dependencies one by one
pip install fastapi
pip install uvicorn[standard]
pip install google-generativeai
pip install PyPDF2 python-multipart python-dotenv
```

### Getting Help

- Check server logs for detailed error messages
- Test with `/health` endpoint first
- Verify API is accessible at http://localhost:8000/docs
- Ensure you're in the correct directory (`main/backend`)

## 🤖 AI Model Information

### Google Gemini 2.5 Flash

- **Model**: `gemini-2.5-flash`
- **Provider**: Google AI Studio
- **Features**: Advanced text analysis, citation generation, legal document processing
- **Specialization**: Parole hearing transcript analysis with line-number citations

### Citation System

The AI generates precise citations for all facts and quotes with both page and line numbers:

- **Direct Quotes**: `"Quote text" - (Speaker Name, Page X, Line Y)`
- **Factual References**: `Information found at Page X, Lines Y-Z`
- **Multi-line References**: `Page X, Lines Y-Z`

Example output:

```markdown
## Parole Factors Cited

- "You can't get any more 115s" - (Commissioner Ruff, Page 5, Line 245)
- Classification score: "68 points" - (Emmanuel Young, Page 1, Line 4)
- Crime details found at Page 2, Lines 8-12
```

## 🏗️ Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── pyproject.toml          # Project configuration and dependencies
├── README.md              # This documentation
├── .env                   # Environment variables (not committed)
├── .gitignore             # Git ignore rules
└── api/                   # API package
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── config.py      # Application configuration & Gemini model setup
    ├── routes/
    │   ├── __init__.py
    │   ├── health.py      # Health check endpoints
    │   └── pdf.py         # PDF processing endpoints with AI prompts
    └── services/
        ├── __init__.py
        └── pdf_service.py # PDF extraction & Gemini AI services
```

## 🛠️ Development

### Adding New Features

1. **New endpoints**: Add to `api/routes/`
2. **Business logic**: Add to `api/services/`
3. **Configuration**: Update `api/core/config.py`

### Code Style

```bash
# Format code
black .
isort .

# Run tests (when available)
pytest
```

### Environment Variables

| Variable         | Description              | Default   |
| ---------------- | ------------------------ | --------- |
| `GEMINI_API_KEY` | Google Gemini AI API key | Required  |
| `HOST`           | Server host              | `0.0.0.0` |
| `PORT`           | Server port              | `8000`    |
| `DEBUG`          | Debug mode               | `True`    |

## 🚀 Deployment

### Docker (Optional)

```bash
# Build image
docker build -t pdf-backend .

# Run container
docker run -p 8000:8000 --env-file .env pdf-backend
```

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use environment-specific API keys
- [ ] Set up proper logging
- [ ] Configure HTTPS
- [ ] Set up monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Hack for Social Impact initiative.

---

**Need help?** Open an issue or contact the development team.
