from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class APIModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Species(str, Enum):
    ATLANTIC_SALMON = "atlantic_salmon"
    RAINBOW_TROUT = "rainbow_trout"
    TOY_FISH = "toy_fish"
    COHO_SALMON = "coho_salmon"


class NewCollection(APIModel):
    name: str
    pen_id: str
    species: Species
    location: str | None = None
    notes: str | None = None


class Collection(APIModel):
    id: int
    name: str
    archived: bool
    location: str
    notes: str | None = None
    pen_id: str
    species: Species
    created_at: datetime
    updated_at: datetime


class CollectionSummary(APIModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    num_fish: int
    avg_weight: float | None


class Fish(APIModel):
    fish_id: str
    collection_id: int
    weight_g: float
    length_mm: float
    width_mm: float | None = None
    breadth_mm: float | None = None
    circumference_mm: float | None = None
    capture_start: datetime
    capture_end: datetime
    sedation_end: datetime
    measurement_end: datetime
    notes: str | None = None


class NewFish(APIModel):
    """Schema for creating a new fish (collection_id comes from URL path)."""
    fish_id: str
    weight_g: float
    length_mm: float
    width_mm: float | None = None
    breadth_mm: float | None = None
    circumference_mm: float | None = None
    capture_start: datetime
    capture_end: datetime
    sedation_end: datetime
    measurement_end: datetime
    notes: str | None = None


class UpdateFish(APIModel):
    """Schema for updating fish measurements."""
    weight_g: float
    length_mm: float
    width_mm: float | None = None
    breadth_mm: float | None = None
    notes: str | None = None