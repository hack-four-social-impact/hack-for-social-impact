from fastapi import APIRouter

from api.core.config import config

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """API root endpoint."""
    return {"message": "PDF Processing API with Gemini Integration"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "gemini_configured": config.is_gemini_configured()}
