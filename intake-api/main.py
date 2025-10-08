from datetime import datetime, timezone
from pathlib import Path

import numpy as np
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
    df.to_csv(filename, index=False)

    logger.info(f"Saved {len(request.fish)} fish.")
    

@app.get("/collections")
def collections():
    collection_dirs = sorted(SAVE_DIR.glob("*"))
    
    collections = []
    for collection_dir in collection_dirs:
        if not (collection_dir / "gtsf_latest.csv").exists():
            continue
        
        df = pd.read_csv(collection_dir / "gtsf_latest.csv")
        
        collections.append({
            "name": collection_dir.name,
            "numFish": len(df),
            "avgWeight": df["weight"].mean(),
        })
    
    print(collections)
    return collections


@app.get("/collection/{collection_name}")
def collection(collection_name: str):
    entries = pd.read_csv(SAVE_DIR / collection_name / "gtsf_latest.csv")
    
    if "Unnamed: 0" in entries.columns:
        entries = entries.drop(columns=["Unnamed: 0"])
    
    entries = (
        entries
        .replace({np.nan:None})
        .to_dict(orient="records")
    )

    return entries