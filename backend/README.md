# Backend API

A FastAPI-based backend server with PDF processing and Google Gemini AI integration.

## Prerequisites

- Python 3.13 or higher
- pip (Python package installer)
- Google Gemini API key (for AI features)

## Setup

1. **Navigate to the backend directory**

   ```bash
   cd main/backend
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install fastapi uvicorn[standard] google-generativeai PyPDF2 python-multipart python-dotenv
   ```

   Or if you have the project configured with pyproject.toml:

   ```bash
   pip install -e .
   ```

4. **Configure environment variables**

   Copy the example environment file and configure your API keys:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Google Gemini API key:

   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn main:app --reload
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Custom Host and Port

```bash
uvicorn main:app --host 127.0.0.1 --port 3001 --reload
```

## Accessing the API

- **API Base URL**: `http://localhost:8000`
- **Interactive API Documentation (Swagger)**: `http://localhost:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Available Endpoints

### Basic Endpoints

- `GET /` - Returns API information
- `GET /health` - Health check endpoint with Gemini configuration status

### PDF Processing Endpoints

- `POST /pdf/process` - Upload a PDF file and process it with Google Gemini AI

  - **Parameters:**
    - `file`: PDF file (required)
    - `prompt`: Custom prompt for AI analysis (optional, default: "Please summarize this document")
    - `max_tokens`: Maximum tokens for response (optional, default: 1000)
  - **Response:** Extracted text and Gemini AI analysis

- `POST /pdf/extract-text` - Extract text from PDF without AI processing
  - **Parameters:**
    - `file`: PDF file (required)
  - **Response:** Extracted text only

### Example Usage

#### Using curl to process a PDF with Gemini:

```bash
curl -X POST "http://localhost:8000/pdf/process" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "prompt=Summarize the key points of this document"
```

#### Using curl to extract text only:

```bash
curl -X POST "http://localhost:8000/pdf/extract-text" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
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

## Troubleshooting

- **Port already in use**: Change the port using `--port` flag or kill the process using the port
- **Module not found**: Make sure you're in the correct directory and dependencies are installed
- **Permission denied**: On macOS/Linux, you might need to use `sudo` or check file permissions
- **Gemini API errors**:
  - Check that your API key is correct in the `.env` file
  - Verify your API key has proper permissions
  - Check your API usage limits
- **PDF processing errors**:
  - Ensure the file is a valid PDF
  - Check file size (10MB limit)
  - Verify the PDF contains extractable text (not just images)

## Next Steps

- Add database integration
- Implement authentication
- Add logging and monitoring
- Create additional API endpoints
- Add tests
