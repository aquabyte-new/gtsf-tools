from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SAVE_DIR = Path("/tmp/gtsf")


class SaveRequest(BaseModel):
    collectionName: str
    fish: list[dict]


app = FastAPI()

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
    return {"message": "GTSF backend is running."}


@app.post("/save")
def save(request: SaveRequest):
    logger.info(f"Saving {len(request.fish)} fish to {request.collectionName}.")

    if len(request.fish) == 0:
        logger.warning("No fish to save.")
        return
    
    # Load data into a DataFrame.
    df = pd.DataFrame(request.fish)
    print(df)

    # Save to CSV.
    collection_dir = SAVE_DIR / request.collectionName.replace(" ", "_").lower()
    
    if not collection_dir.exists():
        logger.info(f"Creating collection directory {collection_dir}.")
        collection_dir.mkdir(parents=True, exist_ok=True)
    
    # Save latest CSV.
    filename = collection_dir / f"gtsf_latest.csv"
    df.to_csv(filename)
    
    # Save timestamped CSV.
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = collection_dir / f"gtsf_{ts}.csv"
    df.to_csv(filename)

    logger.info(f"Saved {len(request.fish)} fish.")