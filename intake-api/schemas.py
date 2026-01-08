from datetime import datetime
from pydantic import BaseModel


class SaveRequest(BaseModel):
    """Request model for saving fish collection data."""
    collectionName: str
    collectionPenId: str
    collectionSpecies: str
    collectionLocation: str | None = None
    collectionNotes: str | None = None
    fish: list[dict]


class Collection(BaseModel):
    """Model for collection summary data."""
    name: str
    numFish: int
    avgWeight: float


class Fish(BaseModel):
    """Model for individual fish data."""
    fishId: str | None
    weight: float
    length: float
    width: float | None
    breadth: float | None
    circumference: float | None
    intakeStart: str
    intakeEnd: str
    sedationEnd: str
    measurementEnd: str
    notes: str | None
