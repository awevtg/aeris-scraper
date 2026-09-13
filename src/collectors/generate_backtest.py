import json
import random
from datetime import date, timedelta
from pathlib import Path

from src.collectors.demo_collector import collect_demo_fare
from src.routes import ROUTES, BOOKING_WINDOWS


OUTPUT = Path("data/raw/backtest_airfares.json")


def main():
    random.seed(42)

    observations = []

    start_date = date.today() - timedelta(days=29)

    for day_number in range(30):

        collection_date = start_date + timedelta(days=day_number)

        for route_index, route in enumerate(ROUTES):

            for booking_window in BOOKING_WINDOWS:

                # Base route-specific fare.
                base_fare = (
                    4000
                    + route_index * 350
                    + booking_window * 25
                )

                # Gradual market movement.
                trend = 1 + (day_number * 0.002)

                # Small random daily movement.
                noise = random.uniform(0.97, 1.03)

                # Create a few controlled airfare surges.
                surge = 1.0

                if day_number in [10, 11, 12]:
                    surge = 1.08

                if day_number in [23, 24, 25]:
                    surge = 1.12

                fare = round(
                    base_fare
                    * trend
                    * noise
                    * surge,
                    2,
                )

                observation = collect_demo_fare(
                    origin=route["origin"],
                    destination=route["destination"],
                    carrier="DEMO",
                    travel_date=(
                        collection_date
                        + timedelta(days=booking_window)
                    ).isoformat(),
                    booking_window=booking_window,
                    total_fare=fare,
                )

                # Replace collection timestamp with
                # the simulated historical date.
                observation_data = observation.model_dump(mode="json")

                observation_data["collected_at"] = (
                    collection_date.isoformat()
                    + "T10:00:00"
                )

                observations.append(observation_data)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w") as f:
        json.dump(observations, f, indent=2)

    print(
        f"Saved {len(observations)} observations "
        f"to {OUTPUT}"
    )


if __name__ == "__main__":
    main()
