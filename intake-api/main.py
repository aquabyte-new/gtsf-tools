import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import db
from api.collections import router as collections_router
from api.samples import router as samples_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow requests from the UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for internal tool
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up API routes
api_router = APIRouter(prefix="/api")
api_router.include_router(collections_router, prefix="/collections")
api_router.include_router(samples_router, prefix="/samples")
app.include_router(api_router)

# Some other helpers.
@app.get("/environment")
async def get_environment() -> str:
    return os.environ.get("ENV", "local")