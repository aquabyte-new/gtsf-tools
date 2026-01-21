from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection

from schemas import Fish, NewFish, UpdateFish
from db import get_conn


router = APIRouter()


@router.get("/{collection_id}")
async def get_samples(
    collection_id: int,
    conn: Connection = Depends(get_conn)
) -> list[Fish]:
    res = await conn.fetch("select * from gtsf_fish where collection_id = $1", collection_id)
    return [Fish(**dict(row)) for row in res]


@router.post("/{collection_id}")
async def create_fish(
    collection_id: int,
    fish: NewFish,
    conn: Connection = Depends(get_conn)
) -> dict[str, str]:
    """Create a new fish in a collection. Uses upsert to handle duplicate fish_id."""

    # Verify collection exists
    collection = await conn.fetchrow(
        "select id, archived from gtsf_collections where id = $1",
        collection_id
    )
    print(collection)
    print(collection['archived'])
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found.")
    if collection['archived']:
        raise HTTPException(status_code=400, detail="Collection is archived.")

    # Upsert fish (insert or update on conflict)
    await conn.execute(
        """
        insert into gtsf_fish (
            fish_id, collection_id, weight_g, length_mm, width_mm, breadth_mm,
            circumference_mm, capture_start, capture_end, sedation_end,
            measurement_end, notes
        ) values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        on conflict (fish_id) do update set
            weight_g = excluded.weight_g,
            length_mm = excluded.length_mm,
            width_mm = excluded.width_mm,
            breadth_mm = excluded.breadth_mm,
            circumference_mm = excluded.circumference_mm,
            capture_start = excluded.capture_start,
            capture_end = excluded.capture_end,
            sedation_end = excluded.sedation_end,
            measurement_end = excluded.measurement_end,
            notes = excluded.notes
        """,
        fish.fish_id,
        collection_id,
        fish.weight_g,
        fish.length_mm,
        fish.width_mm,
        fish.breadth_mm,
        fish.circumference_mm,
        fish.capture_start,
        fish.capture_end,
        fish.sedation_end,
        fish.measurement_end,
        fish.notes
    )

    return {"fishId": fish.fish_id}


@router.patch("/{collection_id}/{fish_id}")
async def update_fish(
    collection_id: int,
    fish_id: str,
    updates: UpdateFish,
    conn: Connection = Depends(get_conn)
) -> dict[str, str]:
    """Update measurements for an existing fish."""

    # Verify fish exists
    existing = await conn.fetchrow(
        "select fish_id from gtsf_fish where fish_id = $1 and collection_id = $2",
        fish_id, collection_id
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Fish not found.")

    await conn.execute(
        """
        update gtsf_fish
        set weight_g = $1, length_mm = $2, width_mm = $3, breadth_mm = $4, notes = $5
        where fish_id = $6 and collection_id = $7
        """,
        updates.weight_g,
        updates.length_mm,
        updates.width_mm,
        updates.breadth_mm,
        updates.notes,
        fish_id,
        collection_id
    )

    return {"fishId": fish_id}