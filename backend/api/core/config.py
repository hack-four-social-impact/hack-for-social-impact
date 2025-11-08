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

    # CORS settings
    ALLOWED_ORIGINS = ["*"]  # Configure this properly in production

    @classmethod
    def get_gemini_model(cls) -> Any:
        """Get configured Gemini model."""
        if GENAI_AVAILABLE and genai and cls.GEMINI_API_KEY:
            try:
                genai.configure(api_key=cls.GEMINI_API_KEY)  # type: ignore
                # Use the basic gemini-pro model which should be available
                return genai.GenerativeModel("gemini-pro")  # type: ignore
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
