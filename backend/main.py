from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.config import config
from api.routes import health, pdf

# Create FastAPI app
app = FastAPI(title=config.API_TITLE, version=config.API_VERSION)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(pdf.router)
