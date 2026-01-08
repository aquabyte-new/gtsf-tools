from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import Database
from schemas import SaveRequest, Collection, Fish

# Database instance
db = Database()


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


@app.get("/")
def ping():
    """Health check endpoint."""
    return {"message": "GTSF backend is running."}


@app.post("/save")
async def save(request: SaveRequest) -> dict:
    """Save collection and fish data."""
    return await db.save_collection(request)


@app.get("/collections")
async def collections() -> list[Collection]:
    """Get all collections with summary statistics."""
    return await db.get_collections()


@app.get("/collection/{collection_name}")
async def collection(collection_name: str) -> list[Fish]:
    """Get all fish data for a specific collection."""
    fish_list = await db.get_collection_fish(collection_name)

    if fish_list is None:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' not found"
        )

    return fish_list
