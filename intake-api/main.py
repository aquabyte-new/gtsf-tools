from datetime import datetime
from contextlib import asynccontextmanager

import asyncpg
from loguru import logger
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Database connection pool
db_pool = None


class SaveRequest(BaseModel):
    collectionName: str
    collectionPenId: str
    collectionSpecies: str
    collectionLocation: str | None = None
    collectionNotes: str | None = None
    fish: list[dict]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database connection pool lifecycle."""
    global db_pool
    logger.info("Connecting to PostgreSQL database...")
    db_pool = await asyncpg.create_pool(
        host="localhost",
        database="postgres",
        user="sam",
        min_size=1,
        max_size=10,
    )
    logger.info("Database connection pool created.")
    yield
    logger.info("Closing database connection pool...")
    await db_pool.close()
    logger.info("Database connection pool closed.")


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
    return {"message": "GTSF backend is running."}


@app.post("/save")
async def save(request: SaveRequest):
    logger.info(f"Saving {len(request.fish)} fish to {request.collectionName}.")

    if len(request.fish) == 0:
        logger.warning("No fish to save.")
        return {"status": "ok", "message": "No fish to save"}

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            # Insert or update collection
            collection_id = await conn.fetchval(
                """
                INSERT INTO gtsf_collections (name, pen_id, species, location, notes)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (name) DO UPDATE SET
                    pen_id = EXCLUDED.pen_id,
                    species = EXCLUDED.species,
                    location = EXCLUDED.location,
                    notes = EXCLUDED.notes,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
                """,
                request.collectionName,
                request.collectionPenId,
                request.collectionSpecies,
                request.collectionLocation,
                request.collectionNotes,
            )

            # Delete existing fish for this collection (we're replacing them)
            await conn.execute(
                "DELETE FROM gtsf_fish WHERE collection_id = $1",
                collection_id
            )

            # Insert all fish
            fish_records = []
            for fish in request.fish:
                fish_records.append((
                    collection_id,
                    fish.get("fishId"),
                    float(fish["weight"]),
                    float(fish["length"]),
                    float(fish.get("width")) if fish.get("width") else None,
                    float(fish.get("breadth")) if fish.get("breadth") else None,
                    float(fish.get("circumference")) if fish.get("circumference") else None,
                    datetime.fromisoformat(fish["intakeStart"].replace("Z", "+00:00")),
                    datetime.fromisoformat(fish["intakeEnd"].replace("Z", "+00:00")),
                    datetime.fromisoformat(fish["sedationEnd"].replace("Z", "+00:00")),
                    datetime.fromisoformat(fish["measurementEnd"].replace("Z", "+00:00")),
                    fish.get("notes"),
                ))

            await conn.executemany(
                """
                INSERT INTO gtsf_fish (
                    collection_id, fish_id, weight_g, length_mm, width_mm, breadth_mm,
                    circumference, intake_start, intake_end, sedation_end, measurement_end, notes
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                """,
                fish_records
            )

    logger.info(f"Saved {len(request.fish)} fish to database.")
    return {"status": "ok", "message": f"Saved {len(request.fish)} fish"}
    

@app.get("/collections")
async def collections():
    async with db_pool.acquire() as conn:
        # Query collections with aggregated fish data
        rows = await conn.fetch(
            """
            SELECT
                c.name,
                COUNT(f.collection_id) as num_fish,
                AVG(f.weight_g) as avg_weight
            FROM gtsf_collections c
            LEFT JOIN gtsf_fish f ON c.id = f.collection_id
            GROUP BY c.id, c.name
            ORDER BY c.name
            """
        )

    collections = [
        {
            "name": row["name"],
            "numFish": row["num_fish"],
            "avgWeight": float(row["avg_weight"]) if row["avg_weight"] is not None else 0.0,
        }
        for row in rows
    ]

    logger.info(f"Retrieved {len(collections)} collections.")
    return collections


@app.get("/collection/{collection_name}")
async def collection(collection_name: str):
    async with db_pool.acquire() as conn:
        # Get collection ID
        collection_id = await conn.fetchval(
            "SELECT id FROM gtsf_collections WHERE name = $1",
            collection_name
        )

        if collection_id is None:
            raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

        # Get all fish for this collection
        rows = await conn.fetch(
            """
            SELECT
                fish_id as "fishId",
                weight_g as weight,
                length_mm as length,
                width_mm as width,
                breadth_mm as breadth,
                circumference,
                intake_start as "intakeStart",
                intake_end as "intakeEnd",
                sedation_end as "sedationEnd",
                measurement_end as "measurementEnd",
                notes
            FROM gtsf_fish
            WHERE collection_id = $1
            ORDER BY created_at
            """,
            collection_id
        )

    # Convert to dict and handle None values
    entries = []
    for row in rows:
        entry = dict(row)
        # Convert datetime objects to ISO format strings
        for key in ["intakeStart", "intakeEnd", "sedationEnd", "measurementEnd"]:
            if entry[key] is not None:
                entry[key] = entry[key].isoformat()
        entries.append(entry)

    logger.info(f"Retrieved {len(entries)} fish from collection '{collection_name}'.")
    return entries