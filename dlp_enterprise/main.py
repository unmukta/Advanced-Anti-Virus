# dlp_enterprise/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(\"DATABASE_URL\", \"postgresql+asyncpg://dlp_user:dlp_password@localhost:5432/dlp_enterprise\")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=\"token\")

@asynccontextmanager
async def lifespan(app: FastAPI):
    \"\"\"Application lifespan context manager\"\"\"
    # Startup: Create database tables
    try:
        from dlp.models.base import Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(\"Database tables created successfully\")
    except Exception as e:
        logger.error(f\"Database initialization error: {e}\")
    
    yield
    
    # Shutdown: Close database connection
    await engine.dispose()
    logger.info(\"Database connection closed\")

# Create FastAPI app
app = FastAPI(
    title=\"DLP Enterprise 3.0\",
    description=\"Next-Generation Data Loss Prevention System\",
    version=\"3.0.0\",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"*\"],
    allow_credentials=True,
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)

# Dependency to get database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Health check endpoint
@app.get(\"/health\")
async def health_check():
    return {\"status\": \"healthy\", \"version\": \"3.0.0\"}

@app.get(\"/api/v1/health\")
async def api_health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Test database connection
        await db.execute(\"SELECT 1\")
        return {\"database\": \"connected\", \"status\": \"healthy\"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f\"Database error: {str(e)}\")

# Authentication endpoint
@app.post(\"/token\")
async def login_for_access_token():
    # TODO: Implement JWT token generation
    return {\"access_token\": \"temp_token\", \"token_type\": \"bearer\"}

if __name__ == \"__main__\":
    import uvicorn
    uvicorn.run(app, host=\"0.0.0.0\", port=5001)
