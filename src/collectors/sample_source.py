from datetime import datetime

from src.collectors.source_adapter import SourceAdapter
from src.models import AirfareObservation


class SampleSourceAdapter(SourceAdapter):
    """
    Sample source adapter used to verify the complete AERIS
    collection pipeline before connecting permitted external sources.
    """

    source_name = "sample_source"

    def collect(
        self,
        origin: str,
        destination: str,
        travel_date: str,
        booking_window: int,
    ):
        total_fare = 5200.0
        base_fare = 3900.0
        taxes = 1040.0
        fees = 260.0

        observation = AirfareObservation(
            observation_id=(
                f"SAMPLE-{origin}-{destination}-"
                f"{travel_date}-{booking_window}"
            ),
            source=self.source_name,
            collected_at=datetime.now(),
            origin=origin,
            destination=destination,
            carrier="SAMPLE",
            travel_date=travel_date,
            booking_window=booking_window,
            total_fare=total_fare,
            base_fare=base_fare,
            taxes=taxes,
            fees=fees,
            fare_class="economy",
            stops=0,
            duration_minutes=135,
            availability_status="available",
        )

        return [observation]


if __name__ == "__main__":
    adapter = SampleSourceAdapter()

    observations = adapter.collect(
        origin="DEL",
        destination="BOM",
        travel_date="2026-10-01",
        booking_window=7,
    )

    print("Source adapter test:")
    for observation in observations:
        print(observation.model_dump())

    print("Sample source: OK")
