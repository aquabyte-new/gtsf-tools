from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection

from schemas import NewCollection, Collection, CollectionSummary, Fish, NewFish
from db import get_conn

router = APIRouter()


@router.post("/")
async def create_collection(
    collection: NewCollection,
    conn: Connection = Depends(get_conn)
) -> dict:
    # Make sure that the collection name is unique (case insensitive).
    res = await conn.fetch("select name from gtsf_collections")
    existing_names = [x['name'].lower() for x in res]
    if collection.name.lower() in existing_names:
        raise HTTPException(status_code=400, detail="Collection name already exists")
    
    # Insert the collection into the database.
    row = await conn.fetchrow(
        "insert into gtsf_collections (name, pen_id, species, location, notes) values ($1, $2, $3, $4, $5) returning id",
        collection.name,
        collection.pen_id,
        collection.species,
        collection.location,
        collection.notes
    )

    return {"collectionId": row["id"]}


@router.get("/")
async def list_collections(
    conn: Connection = Depends(get_conn)
) -> list[CollectionSummary]:
    sql = """
        select 
            c.id
            , c.name
            , c.created_at
            , c.updated_at
            , count(f.fish_id) as num_fish
            , avg(f.weight_g) as avg_weight
        from gtsf_collections c
        left join gtsf_fish f on c.id = f.collection_id
        where not c.archived
        group by c.id
        order by created_at desc
    """
    res = await conn.fetch(sql)
    return [CollectionSummary(**dict(row)) for row in res]


@router.get("/{collection_id}")
async def get_collection(
    collection_id: int,
    conn: Connection = Depends(get_conn)
) -> Collection:
    # Grab the collection via the collection ID.
    res = await conn.fetchrow(
        """
        select * 
        from gtsf_collections 
        where id = $1 
          and not archived
        """,
        collection_id
    )
    if not res:
        raise HTTPException(status_code=404, detail="Collection not found.")

    collection = Collection(**dict(res))
    return collection

