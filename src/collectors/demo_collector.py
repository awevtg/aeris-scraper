from datetime import datetime

from src.models import AirfareObservation


def collect_demo_fare(
    origin: str,
    destination: str,
    carrier: str,
    travel_date: str,
    booking_window: int,
    total_fare: float,
) -> AirfareObservation:

    observation_id = (
        f"{origin}-{destination}-"
        f"{travel_date}-{booking_window}-"
        f"{carrier}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )

    return AirfareObservation(
        observation_id=observation_id,
        source="demo",
        collected_at=datetime.now(),
        origin=origin,
        destination=destination,
        carrier=carrier,
        travel_date=travel_date,
        booking_window=booking_window,
        total_fare=total_fare,
        base_fare=total_fare * 0.75,
        taxes=total_fare * 0.20,
        fees=total_fare * 0.05,
        fare_class="economy",
        stops=0,
        availability_status="available",
    )
