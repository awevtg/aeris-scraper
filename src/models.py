from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AirfareObservation(BaseModel):
    observation_id: str
    source: str
    collected_at: datetime
    origin: str
    destination: str
    carrier: str
    travel_date: str
    booking_window: int
    total_fare: float
    base_fare: Optional[float] = None
    taxes: Optional[float] = None
    fees: Optional[float] = None
    fare_class: Optional[str] = None
    stops: Optional[int] = None
    duration_minutes: Optional[int] = None
    availability_status: str = "available"
