"""
Nuvie Backend API - Main Application Entry Point

IMPROVEMENTS:
- Added CORS middleware with configurable origins
- Added security headers middleware
- Added request ID middleware for tracing
- Added proper health/ready endpoints
- Added OpenAPI documentation configuration
- Added logging configuration
"""

import os
import uuid
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .feed import router as feed_router
from .auth import router as auth_router

# -----------------------
# Logging Configuration
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------
# Environment Configuration
# -----------------------
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"
VERSION = os.getenv("APP_VERSION", "1.0.0")

# CORS origins (comma-separated in env)
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8080"
).split(",")


# -----------------------
# Lifespan Events
# -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info(f"Starting Nuvie Backend API v{VERSION} in {ENVIRONMENT} mode")
    yield
    # Shutdown
    logger.info("Shutting down Nuvie Backend API")


# -----------------------
# Application Factory
# -----------------------
app = FastAPI(
    title="Nuvie Backend API",
    description="AI-Powered Social Movie Recommendation Platform",
    version=VERSION,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
    lifespan=lifespan,
)


# -----------------------
# Security Headers Middleware
# -----------------------
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # HSTS in production
        if ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


# -----------------------
# Request ID Middleware
# -----------------------
class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request for tracing."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


# -----------------------
# Middleware Registration
# -----------------------

# CORS - must be added first
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Total-Count"],
    max_age=600,  # Cache preflight for 10 minutes
)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# Request ID tracking
app.add_middleware(RequestIDMiddleware)


# -----------------------
# Exception Handlers
# -----------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception(f"Unhandled exception [request_id={request_id}]: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "request_id": request_id,
            }
        },
    )


# -----------------------
# Routers
# -----------------------
app.include_router(auth_router)
app.include_router(feed_router)


# -----------------------
# Health & Status Endpoints
# -----------------------
@app.get("/health", tags=["System"])
def health():
    """
    Health check endpoint for load balancers and orchestration.

    Returns 200 if the service is running.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
    }


@app.get("/ready", tags=["System"])
def ready():
    """
    Readiness check endpoint.

    Returns 200 if the service is ready to accept traffic.
    This can be extended to check database connectivity, etc.
    """
    # TODO: Add database connectivity check
    # TODO: Add AI service health check
    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "database": "ok",  # Placeholder
            "ai_service": "ok",  # Placeholder
        }
    }


@app.get("/", tags=["System"])
def root():
    """API root - returns basic service info."""
    return {
        "service": "Nuvie Backend API",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "docs": "/docs" if DEBUG else None,
    }
