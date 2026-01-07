from datetime import datetime, timezone
from io import BytesIO, StringIO

import aioboto3
import numpy as np
import pandas as pd
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from s3path import S3Path

SAVE_DIR = S3Path("/aquabyte-datasets/gtsf-intake")
s3_session = aioboto3.Session()


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


async def save_csv(df: pd.DataFrame, s3_path: S3Path, index: bool = True):
    """Save a DataFrame to S3 as a CSV file."""
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=index)

    async with s3_session.client("s3") as s3:
        await s3.put_object(
            Bucket=s3_path.bucket,
            Key=s3_path.key,
            Body=csv_buffer.getvalue()
        )


async def read_csv(s3_path: S3Path) -> pd.DataFrame:
    """Read a CSV file from S3 into a DataFrame."""
    async with s3_session.client("s3") as s3:
        response = await s3.get_object(Bucket=s3_path.bucket, Key=s3_path.key)
        body = await response["Body"].read()
        return pd.read_csv(BytesIO(body))


@app.get("/")
def ping():
    return {"message": "GTSF backend is running."}


@app.post("/save")
async def save(request: SaveRequest):
    logger.info(f"Saving {len(request.fish)} fish to {request.collectionName}.")

    if len(request.fish) == 0:
        logger.warning("No fish to save.")
        return

    # Load data into a DataFrame.
    df = pd.DataFrame(request.fish)
    print(df)

    # Save to CSV in S3.
    collection_dir = SAVE_DIR / request.collectionName.replace(" ", "_").lower()

    # Save latest CSV (with index).
    await save_csv(df, collection_dir / "gtsf_latest.csv", index=True)

    # Save timestamped CSV (without index).
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    await save_csv(df, collection_dir / f"gtsf_{ts}.csv", index=False)

    logger.info(f"Saved {len(request.fish)} fish to S3.")
    

@app.get("/collections")
async def collections():
    async with s3_session.client("s3") as s3:
        # List all objects in the S3 bucket under SAVE_DIR prefix.
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=SAVE_DIR.bucket, Prefix=SAVE_DIR.key + "/")

        collection_names = set()
        async for page in pages:
            if "Contents" not in page:
                continue
            for obj in page["Contents"]:
                key = obj["Key"]
                if key.endswith("/gtsf_latest.csv"):
                    # Extract collection name from path like "gtsf-intake/collection_name/gtsf_latest.csv"
                    parts = key.split("/")
                    if len(parts) >= 2:
                        collection_names.add(parts[-2])

    # Read data for each collection.
    collections = []
    for collection_name in sorted(collection_names):
        try:
            df = await read_csv(SAVE_DIR / collection_name / "gtsf_latest.csv")
            collections.append({
                "name": collection_name,
                "numFish": len(df),
                "avgWeight": df["weight"].mean(),
            })
        except Exception as e:
            logger.warning(f"Failed to read collection {collection_name}: {e}")
            continue

    print(collections)
    return collections


@app.get("/collection/{collection_name}")
async def collection(collection_name: str):
    entries = await read_csv(SAVE_DIR / collection_name / "gtsf_latest.csv")

    if "Unnamed: 0" in entries.columns:
        entries = entries.drop(columns=["Unnamed: 0"])

    entries = (
        entries
        .replace({np.nan:None})
        .to_dict(orient="records")
    )

    return entries