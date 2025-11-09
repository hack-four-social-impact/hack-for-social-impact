import os
from typing import Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai  # type: ignore

    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False


class Config:
    """Application configuration."""

    # API Configuration
    API_TITLE = "PDF Processing API"
    API_VERSION = "1.0.0"

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # File upload limits
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    # Debug mode (disable in production)
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    # CORS settings
    # In production, set ALLOWED_ORIGINS environment variable to your frontend domain
    # Example: ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-app-staging.vercel.app
    _origins = os.getenv("ALLOWED_ORIGINS", "*")
    ALLOWED_ORIGINS = [origin.strip() for origin in _origins.split(",") if origin.strip()]

    @classmethod
    def get_gemini_model(cls) -> Any:
        """Get configured Gemini model."""
        if GENAI_AVAILABLE and genai and cls.GEMINI_API_KEY:
            try:
                genai.configure(api_key=cls.GEMINI_API_KEY)  # type: ignore
                # Use the updated gemini-2.5-flash model
                return genai.GenerativeModel("gemini-2.5-flash")  # type: ignore
            except Exception as e:
                print(f"Error configuring Gemini: {e}")
                return None
        else:
            if not GENAI_AVAILABLE:
                print("Warning: google-generativeai package not installed properly")
            if not cls.GEMINI_API_KEY:
                print("Warning: GEMINI_API_KEY not found in environment variables")
            return None

    @classmethod
    def is_gemini_configured(cls) -> bool:
        """Check if Gemini is properly configured."""
        return cls.GEMINI_API_KEY is not None and GENAI_AVAILABLE


config = Config()
