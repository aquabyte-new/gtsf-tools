from datetime import datetime
from contextlib import asynccontextmanager

import asyncpg
from loguru import logger

from schemas import SaveRequest, Collection, Fish


class Database:
    """Database operations for GTSF intake API."""

    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self, host: str = "localhost", database: str = "postgres", user: str = "sam"):
        """Create database connection pool."""
        logger.info("Connecting to PostgreSQL database...")
        self.pool = await asyncpg.create_pool(
            host=host,
            database=database,
            user=user,
            min_size=1,
            max_size=10,
        )
        logger.info("Database connection pool created.")

    async def disconnect(self):
        """Close database connection pool."""
        if self.pool:
            logger.info("Closing database connection pool...")
            await self.pool.close()
            logger.info("Database connection pool closed.")

    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def save_collection(self, request: SaveRequest) -> dict:
        """Save collection and fish data to database."""
        logger.info(f"Saving {len(request.fish)} fish to {request.collectionName}.")

        if len(request.fish) == 0:
            logger.warning("No fish to save.")
            return {"status": "ok", "message": "No fish to save"}

        async with self.transaction() as conn:
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
            fish_records = [
                (
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
                )
                for fish in request.fish
            ]

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

    async def get_collections(self) -> list[Collection]:
        """Get all collections with aggregated fish data."""
        async with self.pool.acquire() as conn:
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
            Collection(
                name=row["name"],
                numFish=row["num_fish"],
                avgWeight=float(row["avg_weight"]) if row["avg_weight"] is not None else 0.0,
            )
            for row in rows
        ]

        logger.info(f"Retrieved {len(collections)} collections.")
        return collections

    async def get_collection_fish(self, collection_name: str) -> list[Fish]:
        """Get all fish for a specific collection."""
        async with self.pool.acquire() as conn:
            # Get collection ID
            collection_id = await conn.fetchval(
                "SELECT id FROM gtsf_collections WHERE name = $1",
                collection_name
            )

            if collection_id is None:
                return None

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

        # Convert to Fish models
        fish_list = []
        for row in rows:
            fish_data = dict(row)
            # Convert datetime objects to ISO format strings
            for key in ["intakeStart", "intakeEnd", "sedationEnd", "measurementEnd"]:
                if fish_data[key] is not None:
                    fish_data[key] = fish_data[key].isoformat()
            fish_list.append(Fish(**fish_data))

        logger.info(f"Retrieved {len(fish_list)} fish from collection '{collection_name}'.")
        return fish_list
