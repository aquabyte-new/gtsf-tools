from datetime import datetime
from pathlib import Path

import pandas as pd
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

SAVE_DIR = Path("/tmp")


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
def save(fish: list[dict]):
    logger.info(f"Saving {len(fish)} fish.")

    if len(fish) == 0:
        logger.warning("No fish to save.")
        return
    
    # Load data into a DataFrame.
    df = pd.DataFrame(fish)
    print(df)

    # Save to CSV.
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = SAVE_DIR / f"gtsf_{ts}.csv"
    df.to_csv(filename)
    logger.info(f"Saved {len(fish)} fish to {filename}.")