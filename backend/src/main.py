"""
FastAPI application entry point for Phase II Full-Stack Web Application

Per @specs/002-phase2-webapp/plan.md Phase 2: Foundational - Create base FastAPI application with CORS configuration
"""

import sys
import os
from pathlib import Path

# Add the project root to PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config import Settings, get_engine
from src.api.routes import auth, tasks
from src.api.security import SecurityError


# Create FastAPI app
app = FastAPI(
    title="Evolution of Todo - Phase II",
    description="Full-stack multi-user todo application with persistent storage and JWT authentication",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS Middleware Configuration
settings = Settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # Content-Security-Policy removed for local development to avoid fetch blocks
    return response


# Include routers
app.include_router(auth.router, prefix=settings.API_PREFIX + "/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix=settings.API_PREFIX + "/tasks", tags=["Tasks"])


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "2.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Evolution of Todo API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Custom exception handlers
@app.exception_handler(SecurityError)
async def security_exception_handler(request, exc):
    """Handle security exceptions (401 errors)"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "AUTHENTICATION_FAILED",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors (500 errors) with details for debugging"""
    import traceback
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc),
                "trace": traceback.format_exc() if os.getenv("DEBUG") else None
            }
        }
    )


# Startup event - initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database connection and create tables on startup"""
    from sqlmodel import SQLModel
    # Import models to ensure they are registered with SQLModel
    from src.models.user import User
    from src.models.tasks import Task

    engine = get_engine()
    SQLModel.metadata.create_all(engine)


# Shutdown event - cleanup database connections
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup database connections on shutdown"""
    pass


if __name__ == "__main__":
    import uvicorn
    settings = Settings()
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
